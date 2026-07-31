from __future__ import annotations

import os
from io import BytesIO, StringIO
from typing import Any, Dict, List, Optional

import pandas as pd

from src.network.fixtures.utils import match_fixture_teams
from src.preprocessing.utils.inputs import construct_inputs_by_fixture
from src.preprocessing.utils.target import TargetType, class_names, is_binary_target
from web.services.leagues import get_league, load_league_frame
from web.services.models import load_trained_model


def scrape_fixtures(league_id: str, date_str: str) -> pd.DataFrame:
    """Scrape FootyStats fixtures for a league/date. Requires Selenium profile."""
    league = get_league(league_id)
    if league is None:
        raise ValueError("League not found")
    if not getattr(league, "fixture", None):
        raise ValueError("This league has no FootyStats fixture URL configured.")

    # Prefer headless in Docker / VPS
    os.environ.setdefault("FOOTYSTATS_HEADLESS", "1")
    from src.network.fixtures.footystats.scraper import FootyStatsScraper

    scraper = FootyStatsScraper()
    try:
        ok = scraper.load_page(fixture_url=league.fixture)
        if not ok:
            raise RuntimeError("Failed to load FootyStats page (network or timeout).")
        fixtures = scraper.parse_fixture_table(date_str=date_str)
        if fixtures is None or fixtures.empty:
            raise RuntimeError(f"No fixtures found for {date_str}.")
        return fixtures
    finally:
        try:
            scraper._web_driver.quit()
        except Exception:
            pass


def parse_fixtures_csv(content: bytes) -> pd.DataFrame:
    """CSV columns: Home, Away, 1, X, 2 (optional Date)."""
    text = content.decode("utf-8-sig")
    df = pd.read_csv(StringIO(text))
    required = {"Home", "Away", "1", "X", "2"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {', '.join(sorted(missing))}")
    return df


def predict_fixtures(
    *,
    league_id: str,
    model_id: str,
    fixtures: pd.DataFrame,
) -> Dict[str, Any]:
    df = load_league_frame(league_id)
    if df is None:
        raise ValueError("League not found")
    df = df.dropna().reset_index(drop=True)

    model, config = load_trained_model(league_id, model_id)
    if model is None:
        raise ValueError("Model not found")

    matched = match_fixture_teams(fixtures.copy(), df)
    inputs = construct_inputs_by_fixture(df=df, fixture_df=matched)
    y_prob = model.predict_proba(df=inputs)
    y_pred = y_prob.argmax(axis=1)
    labels = class_names(model.target_type)

    rows = []
    for i in range(len(matched)):
        row = {
            "Home": matched.iloc[i]["Home"],
            "Away": matched.iloc[i]["Away"],
            "1": float(matched.iloc[i]["1"]),
            "X": float(matched.iloc[i]["X"]),
            "2": float(matched.iloc[i]["2"]),
            "Predicted": labels[int(y_pred[i])],
        }
        for j, lab in enumerate(labels):
            row[f"Prob({lab})"] = round(float(y_prob[i, j]), 4)
        rows.append(row)

    return {
        "league_id": league_id,
        "model_id": model_id,
        "target_type": model.target_type.value,
        "is_binary": is_binary_target(model.target_type),
        "rows": rows,
        "count": len(rows),
    }


def export_fixture_rows(rows: List[Dict[str, Any]], fmt: str = "csv") -> bytes:
    export_df = pd.DataFrame(rows)
    if fmt == "xlsx":
        buf = BytesIO()
        export_df.to_excel(buf, index=False)
        return buf.getvalue()
    return export_df.to_csv(index=False).encode("utf-8")
