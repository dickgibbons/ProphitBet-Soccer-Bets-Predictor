from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List

import pandas as pd

from src.preprocessing.utils.inputs import construct_inputs_by_teams
from src.preprocessing.utils.target import TargetType, class_names, is_binary_target
from web.services.leagues import load_league_frame
from web.services.models import load_trained_model


def team_options(league_id: str) -> Dict[str, List[str]]:
    df = load_league_frame(league_id)
    if df is None:
        raise ValueError("League not found")
    return {
        "home": sorted(df["Home"].dropna().unique().tolist()),
        "away": sorted(df["Away"].dropna().unique().tolist()),
    }


def predict_manual(
    *,
    league_id: str,
    model_id: str,
    home: str,
    away: str,
    odd_1: float,
    odd_x: float,
    odd_2: float,
) -> Dict[str, Any]:
    df = load_league_frame(league_id)
    if df is None:
        raise ValueError("League not found")
    df = df.dropna().reset_index(drop=True)

    model, config = load_trained_model(league_id, model_id)
    if model is None:
        raise ValueError("Model not found")

    match_df = pd.DataFrame(
        [{"Home": home, "Away": away, "1": odd_1, "X": odd_x, "2": odd_2}]
    )
    inputs = construct_inputs_by_teams(df=df, match_df=match_df)
    y_pred, _ = model.predict(df=inputs)
    y_prob = model.predict_proba(df=inputs)[0]

    labels = class_names(model.target_type)
    label_map = {i: lab for i, lab in enumerate(labels)}
    probs = {f"Prob({lab})": round(float(y_prob[i]), 4) for i, lab in enumerate(labels)}

    result = {
        "home": home,
        "away": away,
        "odd_1": odd_1,
        "odd_x": odd_x,
        "odd_2": odd_2,
        "predicted": label_map[int(y_pred[0])],
        "target_type": model.target_type.value,
        "is_binary": is_binary_target(model.target_type),
        **probs,
    }
    return result


def export_predictions(rows: List[Dict[str, Any]], fmt: str = "csv") -> bytes:
    export_df = pd.DataFrame(rows)
    if fmt == "xlsx":
        buf = BytesIO()
        export_df.to_excel(buf, index=False)
        return buf.getvalue()
    return export_df.to_csv(index=False).encode("utf-8")
