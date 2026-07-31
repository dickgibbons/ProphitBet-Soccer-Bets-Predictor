from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from src.database.league import LeagueDatabase
from src.database.model import ModelDatabase
from src.network.leagues.league import League
from src.preprocessing.statistics import StatisticsEngine
from web import db as web_db

_league_db: Optional[LeagueDatabase] = None

MANDATORY_COLUMNS = {"Date", "Season", "Home", "Away", "HG", "AG", "Result", "1", "X", "2"}


def get_league_db() -> LeagueDatabase:
    global _league_db
    if _league_db is None:
        _league_db = LeagueDatabase()
    return _league_db


def refresh_league_db() -> LeagueDatabase:
    global _league_db
    _league_db = LeagueDatabase()
    return _league_db


def available_league_templates() -> List[Dict[str, Any]]:
    ldb = get_league_db()
    return [
        {
            "index": i,
            "country": league.country,
            "name": league.name,
            "category": league.category,
            "start_year": league.start_year,
            "label": f"{league.country} — {league.name}",
            "suggested_id": suggest_league_id(league.name, league.country),
        }
        for i, league in enumerate(ldb.leagues)
    ]


def suggest_league_id(name: str, country: str) -> str:
    """Build a readable unique id like Premier-League-England-01."""
    ldb = get_league_db()
    base = f"{name}-{country}".replace(" ", "-")
    # Keep letters, digits, dash, underscore only.
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in base)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    cleaned = cleaned.strip("-") or "league"

    for n in range(1, 100):
        candidate = f"{cleaned}-{n:02d}"
        if not ldb.league_exists(candidate):
            return candidate
    return f"{cleaned}-{date.today().strftime('%Y%m%d')}"


def default_stats_columns(category: str) -> List[str]:
    basic = StatisticsEngine.get_basic_stat_columns()
    if category == "main":
        return basic + StatisticsEngine.get_extended_stat_columns()
    return basic


def list_created_leagues() -> List[Dict[str, Any]]:
    # Reload from disk so leagues created by batch jobs / other processes appear.
    ldb = refresh_league_db()
    rows = []
    for league_id in ldb.get_league_ids():
        league = ldb.index[league_id]
        df = ldb.load_league(league_id)
        rows.append(
            {
                "league_id": league_id,
                "country": league.country,
                "name": league.name,
                "start_year": league.start_year,
                "category": league.category,
                "rows": 0 if df is None else int(df.shape[0]),
            }
        )
    return rows


def load_league_frame(league_id: str) -> Optional[pd.DataFrame]:
    return get_league_db().load_league(league_id=league_id)


def get_league(league_id: str) -> Optional[League]:
    ldb = get_league_db()
    return ldb.index.get(league_id)


def create_league_sync(
    *,
    template_index: int,
    league_id: str,
    start_year: int,
    match_history_window: int = 3,
    goal_diff_margin: int = 2,
    odd_1_range: Optional[Tuple[float, float]] = None,
    odd_x_range: Optional[Tuple[float, float]] = None,
    odd_2_range: Optional[Tuple[float, float]] = None,
    progress_cb=None,
) -> Dict[str, Any]:
    ldb = get_league_db()
    league_id = league_id.strip()
    if not league_id:
        raise ValueError("League id is required.")
    if ldb.league_exists(league_id):
        raise ValueError(f"League id already exists: {league_id}")

    template = ldb.leagues[template_index]
    max_year = date.today().year - 4
    start_year = max(template.start_year, min(start_year, max_year))

    league = template.clone(
        start_year=start_year,
        league_id=league_id,
        match_history_window=match_history_window,
        goal_diff_margin=goal_diff_margin,
        stats_columns=default_stats_columns(template.category),
        odd_1_range=odd_1_range,
        odd_x_range=odd_x_range,
        odd_2_range=odd_2_range,
    )

    if progress_cb:
        progress_cb(0.2, f"Downloading {league.country} {league.name}...")

    df = ldb.create_league(league=league)
    if df is None:
        raise RuntimeError("League download failed. Check internet connection and try again.")

    if progress_cb:
        progress_cb(0.9, f"Saved {df.shape[0]} matches.")

    refresh_league_db()
    return {
        "league_id": league_id,
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
    }


def update_league_sync(league_id: str, progress_cb=None) -> Dict[str, Any]:
    ldb = get_league_db()
    if not ldb.league_exists(league_id):
        raise ValueError(f"Unknown league: {league_id}")
    if progress_cb:
        progress_cb(0.2, f"Updating {league_id}...")
    df = ldb.update_league(league_id=league_id)
    if df is None:
        raise RuntimeError("League update failed. Check internet connection.")
    refresh_league_db()
    if progress_cb:
        progress_cb(0.95, f"Updated to {df.shape[0]} matches.")
    return {"league_id": league_id, "rows": int(df.shape[0])}


def bulk_create_leagues_sync(
    *,
    specs: List[Dict[str, Any]],
    progress_cb=None,
) -> Dict[str, Any]:
    """Create multiple leagues. Each spec: template_index, league_id?, start_year, ..."""
    created = []
    errors = []
    total = max(1, len(specs))
    for i, spec in enumerate(specs):
        if progress_cb:
            progress_cb((i + 0.1) / total, f"Creating league {i+1}/{total}...")
        try:
            tpl_idx = int(spec["template_index"])
            templates = available_league_templates()
            tpl = next(t for t in templates if t["index"] == tpl_idx)
            league_id = (spec.get("league_id") or "").strip() or tpl["suggested_id"]
            result = create_league_sync(
                template_index=tpl_idx,
                league_id=league_id,
                start_year=int(spec.get("start_year", 2018)),
                match_history_window=int(spec.get("match_history_window", 3)),
                goal_diff_margin=int(spec.get("goal_diff_margin", 2)),
            )
            created.append(result)
        except Exception as exc:
            errors.append({"spec": spec, "error": str(exc)})
    return {"created": created, "errors": errors}


def delete_league(league_id: str) -> None:
    ldb = get_league_db()
    if not ldb.league_exists(league_id):
        raise ValueError(f"Unknown league: {league_id}")
    try:
        ModelDatabase(league_id=league_id).delete_league_models()
    except Exception:
        pass
    ldb.delete_league(league_id=league_id)
    web_db.delete_league_model_meta(league_id)
    refresh_league_db()


def filter_matches(
    df: pd.DataFrame,
    *,
    query: str = "",
    hide_missing: bool = False,
) -> pd.DataFrame:
    out = df.copy()
    if hide_missing:
        out = out.dropna()
    if query:
        q = query.strip().lower()
        mask = out.apply(
            lambda row: any(q in str(v).lower() for v in row.values),
            axis=1,
        )
        out = out[mask]
    return out


def dataframe_to_records(df: pd.DataFrame, limit: int = 500) -> List[Dict[str, Any]]:
    view = df.head(limit).copy()
    # Make JSON-friendly
    for col in view.columns:
        if pd.api.types.is_datetime64_any_dtype(view[col]):
            view[col] = view[col].astype(str)
    view = view.where(pd.notnull(view), None)
    return view.to_dict(orient="records")
