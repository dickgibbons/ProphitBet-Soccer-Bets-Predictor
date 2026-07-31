#!/usr/bin/env python3
"""Systematic ProphitBet research: train models, sweep filters, rank Eval edges."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Project root on PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.preprocessing.utils.target import TargetType, construct_targets, is_binary_target
from web.services import evaluate as evaluate_service
from web.services import leagues as league_service
from web.services import models as model_service
from web.services.models import load_trained_model

# Probability percentile grid (0 = no filter). Keep coarse to control runtime.
P_LEVELS = [0, 10, 20, 30, 40]
# For Result: focus one class at a time (betting niche) + a few joint mild filters.
RESULT_P_COMBOS = (
    [{"p1": p, "px": 0, "p2": 0} for p in P_LEVELS]
    + [{"p1": 0, "px": p, "p2": 0} for p in P_LEVELS[1:]]
    + [{"p1": 0, "px": 0, "p2": p} for p in P_LEVELS[1:]]
    + [{"p1": 10, "px": 10, "p2": 10}, {"p1": 20, "px": 10, "p2": 10}]
)
OU_P_COMBOS = (
    [{"pu": p, "po": 0} for p in P_LEVELS]
    + [{"pu": 0, "po": p} for p in P_LEVELS[1:]]
    + [{"pu": 10, "po": 10}, {"pu": 20, "po": 10}]
)

TRAIN_PLAN = [
    ("rf-result", "random_forest", "result"),
    ("xgb-result", "xgboost", "result"),
    ("lr-result", "logistic", "result"),
    ("dt-result", "decision_tree", "result"),
    ("svm-result", "svm", "result"),
    ("rf-ou", "random_forest", "over_under"),
    ("xgb-ou", "xgboost", "over_under"),
    ("rf-ou15", "random_forest", "over_under_15"),
    ("rf-ou35", "random_forest", "over_under_35"),
    ("rf-btts", "random_forest", "btts"),
    ("xgb-btts", "xgboost", "btts"),
]


def _flat_roi(df: pd.DataFrame, y_pred: np.ndarray, filter_mask: np.ndarray, target_type: TargetType) -> Dict[str, float]:
    """Unit-stake ROI if you bet the model's predicted class every filtered match."""
    idx = np.where(filter_mask)[0]
    if len(idx) == 0:
        return {"roi": 0.0, "profit_units": 0.0, "hit_rate": 0.0}
    y_true = construct_targets(df=df, target_type=target_type)[idx]
    pred = y_pred[idx]
    if target_type == TargetType.RESULT:
        odds = df.loc[idx, ["1", "X", "2"]].to_numpy(dtype=float)
        selected = odds[np.arange(len(pred)), pred]
    else:
        # O/U has no dedicated line odds in MVP dataset — skip ROI
        return {"roi": float("nan"), "profit_units": float("nan"), "hit_rate": float((pred == y_true).mean())}
    payout = np.where(pred == y_true, selected - 1.0, -1.0)
    return {
        "roi": float(payout.mean()),
        "profit_units": float(payout.sum()),
        "hit_rate": float((pred == y_true).mean()),
    }


def ensure_models(league_id: str, eval_ratio: float = 0.2) -> List[str]:
    existing = {m["model_id"] for m in model_service.list_models(league_id)}
    trained = []
    for model_id, model_type, target_key in TRAIN_PLAN:
        if model_id in existing:
            print(f"  skip train {model_id} (exists)")
            trained.append(model_id)
            continue
        print(f"  training {model_id} ({model_type}/{target_key})...")
        t0 = time.time()
        try:
            model_service.train_model_sync(
                league_id=league_id,
                model_id=model_id,
                model_type=model_type,
                target_key=target_key,
                eval_ratio=eval_ratio,
            )
            print(f"    done in {time.time() - t0:.1f}s")
            trained.append(model_id)
        except Exception as e:
            print(f"    FAILED: {e}")
    return trained


def sweep_model(league_id: str, model_id: str, min_samples: int = 40) -> List[Dict[str, Any]]:
    model, config = load_trained_model(league_id, model_id)
    if model is None:
        return []

    df = league_service.load_league_frame(league_id)
    if df is None:
        return []
    df = df.dropna().reset_index(drop=True)
    y_prob = model.predict_proba(df=df)
    y_pred = y_prob.argmax(axis=1)

    odd_keys = ["none"] + [str(i) for i in range(1, len(evaluate_service.ODD_RANGES))]
    p_combos = RESULT_P_COMBOS if not is_binary_target(model.target_type) else OU_P_COMBOS

    hits: List[Dict[str, Any]] = []
    for odd_key in odd_keys:
        for perc in p_combos:
            try:
                result = evaluate_service.evaluate_model(
                    league_id=league_id,
                    model_id=model_id,
                    dataset="Eval",
                    odd_range_key=odd_key,
                    percentiles=perc,
                )
            except Exception:
                continue
            m = result["metrics"]
            samples = m["samples"]
            if samples < min_samples:
                continue

            # Rebuild filter mask for ROI (same logic as evaluate_model)
            num_eval = int(config.get("num_eval_samples") or max(1, int(df.shape[0] * 0.2)))
            masks = evaluate_service._dataset_masks(df, num_eval)
            dataset_mask = masks["Eval"]
            odd_mask = np.ones(df.shape[0], dtype=bool)
            odd_label = "none"
            if odd_key not in (None, "", "none"):
                idx = int(odd_key)
                odd, low, high = evaluate_service.ODD_RANGES[idx]
                odd_mask = (df[odd] >= low) & (df[odd] <= high)
                odd_label = f"{odd}-[{low},{high}]"

            if model.target_type == TargetType.RESULT:
                p_vals = [float(perc.get("p1", 0)), float(perc.get("px", 0)), float(perc.get("p2", 0))]
                base = y_prob[dataset_mask & odd_mask]
                thresholds = np.quantile(base, [p / 100 for p in p_vals]) if base.shape[0] else np.zeros(3)
                prob_mask = np.all(y_prob >= thresholds, axis=1)
            else:
                p_vals = [float(perc.get("pu", 0)), float(perc.get("po", 0))]
                base = y_prob[dataset_mask & odd_mask]
                thresholds = np.quantile(base, [p / 100 for p in p_vals]) if base.shape[0] else np.zeros(2)
                prob_mask = np.all(y_prob >= thresholds, axis=1)

            filter_mask = dataset_mask & odd_mask & prob_mask
            roi = _flat_roi(df, y_pred, filter_mask, model.target_type)

            acc = m["accuracy"]
            pb = m["profit_balance"]
            pb_edge = (model.target_type == TargetType.RESULT) and (pb < acc) and (pb > 0)
            roi_val = roi["roi"]
            positive_roi = (not np.isnan(roi_val)) and (roi_val > 0)

            # Score: prefer positive ROI, ProphitBet PB edge, larger samples, higher accuracy
            score = 0.0
            if positive_roi:
                score += 50 + min(roi_val, 0.5) * 100
            if pb_edge:
                score += 20 + max(0.0, acc - pb) * 50
            score += min(samples, 200) / 10.0
            score += acc * 10

            hits.append(
                {
                    "league_id": league_id,
                    "model_id": model_id,
                    "target": model.target_type.value,
                    "odd_range": odd_label,
                    "odd_key": odd_key,
                    "percentiles": perc,
                    "samples": samples,
                    "correct": m["correct"],
                    "accuracy": round(acc, 4),
                    "f1": round(m["f1"], 4),
                    "profit_balance": pb,
                    "pb_edge": pb_edge,
                    "roi": None if np.isnan(roi_val) else round(roi_val, 4),
                    "profit_units": None if np.isnan(roi["profit_units"]) else round(roi["profit_units"], 2),
                    "score": round(score, 2),
                }
            )
    return hits


def create_top_league(name_substr: str, country: str, start_year: int = 2018) -> Optional[str]:
    templates = league_service.available_league_templates()
    match = None
    for t in templates:
        if country.lower() in t["country"].lower() and name_substr.lower() in t["name"].lower():
            match = t
            break
    if match is None:
        print(f"No template for {country}/{name_substr}")
        return None
    league_id = match["suggested_id"]
    if league_service.get_league_db().league_exists(league_id):
        print(f"League exists: {league_id}")
        return league_id
    print(f"Creating {league_id} (start={start_year})...")
    league_service.create_league_sync(
        template_index=match["index"],
        league_id=league_id,
        start_year=start_year,
        match_history_window=3,
        goal_diff_margin=2,
        progress_cb=lambda p, msg: print(f"  [{p:.0%}] {msg}"),
    )
    league_service.refresh_league_db()
    return league_id


def run_league(league_id: str, min_samples: int, top_n: int) -> Dict[str, Any]:
    print(f"\n=== {league_id} ===")
    models = ensure_models(league_id)
    all_hits: List[Dict[str, Any]] = []
    for mid in models:
        print(f"  sweeping {mid}...")
        hits = sweep_model(league_id, mid, min_samples=min_samples)
        print(f"    {len(hits)} candidates ≥ {min_samples} samples")
        all_hits.extend(hits)

    all_hits.sort(key=lambda x: x["score"], reverse=True)
    # Prefer actionable: positive ROI or PB edge
    actionable = [h for h in all_hits if h.get("roi") and h["roi"] > 0] or [h for h in all_hits if h["pb_edge"]]
    if not actionable:
        actionable = all_hits[:top_n]

    return {
        "league_id": league_id,
        "models": models,
        "candidates": len(all_hits),
        "top": actionable[:top_n],
        "baseline": [h for h in all_hits if h["odd_range"] == "none" and max(h["percentiles"].values()) == 0][:5],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--leagues", nargs="*", help="Existing league ids to research")
    parser.add_argument(
        "--create",
        nargs="*",
        help="Create templates as Country:Name e.g. Spain:La-Liga England:Premier-League",
    )
    parser.add_argument("--start-year", type=int, default=2018)
    parser.add_argument("--min-samples", type=int, default=40)
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--out", type=str, default="data/research_results.json")
    args = parser.parse_args()

    league_ids: List[str] = list(args.leagues or [])
    if args.create:
        for item in args.create:
            country, name = item.split(":", 1)
            lid = create_top_league(name, country, start_year=args.start_year)
            if lid:
                league_ids.append(lid)

    if not league_ids:
        league_ids = [L["league_id"] for L in league_service.list_created_leagues()]

    reports = []
    for lid in league_ids:
        reports.append(run_league(lid, args.min_samples, args.top))

    # Cross-league ranking
    flat = []
    for r in reports:
        for h in r["top"]:
            flat.append(h)
    flat.sort(key=lambda x: x["score"], reverse=True)

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "min_samples": args.min_samples,
        "leagues": reports,
        "global_top": flat[:40],
        "notes": [
            "All metrics are on Eval holdout (most recent slice), not Train.",
            "ROI = mean unit-stake profit betting the model's predicted 1/X/2 at book odds.",
            "pb_edge = Profit Balance < Accuracy (ProphitBet's mathematical profitability flag).",
            "Filter fishing inflates false positives — prefer edges that repeat across models/leagues.",
            "Not financial advice; past eval edges can disappear out of sample.",
        ],
    }

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {out_path} ({len(flat)} ranked edges)")
    print("\n=== GLOBAL TOP (actionable) ===")
    for h in flat[:15]:
        print(
            f"{h['league_id'][:28]:28} {h['model_id']:12} "
            f"acc={h['accuracy']:.3f} roi={h['roi']} n={h['samples']} "
            f"odd={h['odd_range']} p={h['percentiles']}"
        )


if __name__ == "__main__":
    main()
