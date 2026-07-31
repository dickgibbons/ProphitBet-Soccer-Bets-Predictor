#!/usr/bin/env python3
"""Create all missing football-data leagues, then research-sweep them."""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from web.services import leagues as league_service
from scripts.research_sweep import ensure_models, run_league

SKIP = {
    ("England", "Premier-League"),
    ("France", "Ligue-1"),
    ("Germany", "Bundesliga-1"),
    ("Italy", "Serie-A"),
    ("Spain", "La-Liga"),
}
START_YEAR = 2018
MIN_SAMPLES = 40
TOP_N = 20
OUT = ROOT / "data" / "research" / "sweep-all-new.json"
LOG = ROOT / "data" / "research" / "batch_all_leagues.log"


def log(msg: str) -> None:
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ") + " " + msg
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def existing_keys():
    return {(L["country"], L["name"]) for L in league_service.list_created_leagues()}


def main():
    LOG.parent.mkdir(parents=True, exist_ok=True)
    templates = league_service.available_league_templates()
    have = existing_keys()
    created_ids = []
    errors = []

    todo = [
        t
        for t in templates
        if (t["country"], t["name"]) not in have and (t["country"], t["name"]) not in SKIP
    ]
    log("Creating %d leagues (start_year=%d)" % (len(todo), START_YEAR))

    for i, t in enumerate(todo, 1):
        lid = t["suggested_id"]
        log("[%d/%d] CREATE %s" % (i, len(todo), lid))
        try:
            league_service.create_league_sync(
                template_index=t["index"],
                league_id=lid,
                start_year=START_YEAR,
                match_history_window=3,
                goal_diff_margin=2,
                progress_cb=lambda p, m: None,
            )
            league_service.refresh_league_db()
            created_ids.append(lid)
            log("  OK %s" % lid)
        except Exception as e:
            errors.append({"league": lid, "stage": "create", "error": str(e)})
            log("  FAIL create %s: %s" % (lid, e))

    research_ids = []
    seen = set()
    for L in league_service.list_created_leagues():
        key = (L["country"], L["name"])
        if key in SKIP:
            continue
        if key in seen:
            continue
        seen.add(key)
        research_ids.append(L["league_id"])

    for lid in created_ids:
        if lid not in research_ids:
            research_ids.append(lid)

    log("Researching %d leagues" % len(research_ids))
    reports = []
    for i, lid in enumerate(research_ids, 1):
        log("[%d/%d] RESEARCH %s" % (i, len(research_ids), lid))
        try:
            ensure_models(lid)
            reports.append(run_league(lid, MIN_SAMPLES, TOP_N))
            log("  OK %s candidates=%s" % (lid, reports[-1].get("candidates")))
        except Exception as e:
            errors.append({"league": lid, "stage": "research", "error": str(e)})
            log("  FAIL research %s: %s" % (lid, e))

    flat = []
    for r in reports:
        flat.extend(r.get("top") or [])
    flat.sort(key=lambda x: x.get("score", 0), reverse=True)

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "created": created_ids,
        "researched": research_ids,
        "errors": errors,
        "min_samples": MIN_SAMPLES,
        "leagues": reports,
        "global_top": flat[:50],
    }
    OUT.write_text(json.dumps(out, indent=2))
    log("Wrote %s top=%d errors=%d" % (OUT, len(out["global_top"]), len(errors)))
    print("=== GLOBAL TOP ===", flush=True)
    for h in flat[:20]:
        print(
            "%-28s %-12s roi=%s n=%s odd=%s"
            % (
                str(h.get("league_id", ""))[:28],
                h.get("model_id", ""),
                h.get("roi"),
                h.get("samples"),
                h.get("odd_range"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
