from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from src.metrics.balance import compute_profit_balance
from src.preprocessing.utils.target import TargetType, class_names, construct_targets, is_binary_target
from web import db as web_db
from web.services.leagues import load_league_frame
from web.services.models import load_trained_model

ODD_RANGES = [
    None,
    ("1", 1.00, 1.3),
    ("1", 1.31, 1.6),
    ("1", 1.61, 1.9),
    ("1", 1.91, 2.5),
    ("1", 2.5, 3.5),
    ("1", 3.51, 100),
    ("X", 1.00, 2.0),
    ("X", 2.0, 3.0),
    ("X", 3.01, 100),
    ("2", 1.00, 1.3),
    ("2", 1.31, 1.6),
    ("2", 1.61, 1.9),
    ("2", 1.91, 2.5),
    ("2", 2.5, 3.5),
    ("2", 3.51, 100),
]


def odd_range_choices() -> List[Dict[str, str]]:
    choices = [{"value": "none", "label": "None"}]
    for i, item in enumerate(ODD_RANGES[1:], start=1):
        odd, low, high = item
        choices.append({"value": str(i), "label": f"{odd}-[{low}, {high}]"})
    return choices


def _dataset_masks(df: pd.DataFrame, num_eval_samples: int) -> Dict[str, np.ndarray]:
    n = df.shape[0]
    all_mask = np.ones(n, dtype=bool)
    eval_mask = np.zeros(n, dtype=bool)
    eval_n = min(max(num_eval_samples, 0), n)
    eval_mask[:eval_n] = True
    train_mask = ~eval_mask
    return {"All": all_mask, "Train": train_mask, "Eval": eval_mask}


def evaluate_model(
    *,
    league_id: str,
    model_id: str,
    dataset: str = "Eval",
    odd_range_key: str = "none",
    percentiles: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    df = load_league_frame(league_id)
    if df is None:
        raise ValueError("League not found")
    df = df.dropna().reset_index(drop=True)

    model, config = load_trained_model(league_id, model_id)
    if model is None or config is None:
        raise ValueError("Model not found")

    num_eval = int(config.get("num_eval_samples") or max(1, int(df.shape[0] * 0.2)))
    masks = _dataset_masks(df, num_eval)
    if dataset not in masks:
        dataset = "All"

    y_prob = model.predict_proba(df=df)
    y_pred = y_prob.argmax(axis=1)
    y_true = construct_targets(df=df, target_type=model.target_type)

    dataset_mask = masks[dataset]
    odd_mask = np.ones(df.shape[0], dtype=bool)
    if odd_range_key not in (None, "", "none"):
        idx = int(odd_range_key)
        odd, low, high = ODD_RANGES[idx]
        odd_mask = (df[odd] >= low) & (df[odd] <= high)

    percentiles = percentiles or {}
    if model.target_type == TargetType.RESULT:
        p_vals = [
            float(percentiles.get("p1", 0)),
            float(percentiles.get("px", 0)),
            float(percentiles.get("p2", 0)),
        ]
        base = y_prob[dataset_mask & odd_mask]
        if base.shape[0] == 0:
            thresholds = np.zeros(3, dtype=np.float32)
        else:
            thresholds = np.quantile(base, [p / 100 for p in p_vals])
        prob_mask = np.all(y_prob >= thresholds, axis=1)
    else:
        p_vals = [
            float(percentiles.get("pu", 0)),
            float(percentiles.get("po", 0)),
        ]
        base = y_prob[dataset_mask & odd_mask]
        if base.shape[0] == 0:
            thresholds = np.zeros(2, dtype=np.float32)
        else:
            thresholds = np.quantile(base, [p / 100 for p in p_vals])
        prob_mask = np.all(y_prob >= thresholds, axis=1)

    filter_mask = dataset_mask & odd_mask & prob_mask
    filtered_true = y_true[filter_mask]
    filtered_pred = y_pred[filter_mask]
    metrics_df = model.compute_metrics(y_true=filtered_true, y_pred=filtered_pred)

    profit_balance = 0.0
    if model.target_type == TargetType.RESULT and filtered_pred.shape[0] > 0:
        odds_df = df.loc[filter_mask, ["1", "X", "2"]].to_numpy()
        selected_odds = odds_df[np.arange(filtered_pred.shape[0]), filtered_pred]
        profit_balance = float(compute_profit_balance(odds=selected_odds))

    labels = class_names(model.target_type)
    mapper = np.array(labels)
    if model.target_type == TargetType.RESULT:
        prob_cols = ["Prob(1)", "Prob(X)", "Prob(2)"]
    else:
        prob_cols = [f"Prob({labels[0]})", f"Prob({labels[1]})"]

    preview = df.loc[filter_mask, ["Date", "Season", "Home", "Away", "Result", "1", "X", "2"]].copy()
    preview["Predicted"] = mapper.take(filtered_pred)
    for i, col in enumerate(prob_cols):
        preview[col] = np.round(y_prob[filter_mask, i], 2)
    preview["Correct"] = filtered_pred == filtered_true

    # Seasonal breakdown
    seasonal = []
    if filter_mask.any() and "Season" in df.columns:
        seas = df.loc[filter_mask, "Season"].astype(str)
        for season in sorted(seas.unique()):
            smask = seas == season
            yt = filtered_true[smask.to_numpy()]
            yp = filtered_pred[smask.to_numpy()]
            if yt.shape[0] == 0:
                continue
            seasonal.append(
                {
                    "season": season,
                    "samples": int(yt.shape[0]),
                    "correct": int((yt == yp).sum()),
                    "accuracy": round(float((yt == yp).mean()), 4),
                }
            )

    preview_records = preview.head(200).where(pd.notnull(preview.head(200)), None).to_dict(orient="records")

    return {
        "metrics": {
            "accuracy": float(metrics_df.at[0, "Accuracy"]),
            "f1": float(metrics_df.at[0, "F1"]),
            "precision": float(metrics_df.at[0, "Precision"]),
            "recall": float(metrics_df.at[0, "Recall"]),
            "samples": int(filtered_pred.shape[0]),
            "correct": int((filtered_pred == filtered_true).sum()),
            "profit_balance": profit_balance,
        },
        "thresholds": [float(x) for x in thresholds],
        "preview": preview_records,
        "seasonal": seasonal,
        "target_type": model.target_type.value,
        "is_binary": is_binary_target(model.target_type),
        "filter_mask_count": int(filter_mask.sum()),
        "_preview_df": preview,  # for export; stripped by routes if needed
    }


def export_filtered_preview(preview_df: pd.DataFrame, fmt: str = "csv") -> bytes:
    if fmt == "xlsx":
        buf = BytesIO()
        preview_df.to_excel(buf, index=False)
        return buf.getvalue()
    return preview_df.to_csv(index=False).encode("utf-8")


def save_filter(league_id: str, model_id: str, name: str, filter_data: Dict[str, Any]) -> None:
    web_db.save_eval_filter(league_id, model_id, name, filter_data)


def list_filters(league_id: str, model_id: str) -> List[Dict[str, Any]]:
    return web_db.list_eval_filters(league_id, model_id)


def delete_filter(filter_id: int) -> None:
    web_db.delete_eval_filter(filter_id)
