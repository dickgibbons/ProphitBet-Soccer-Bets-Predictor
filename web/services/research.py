from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from web.config import PROJECT_ROOT

# Reuse the CLI sweep helpers
from scripts.research_sweep import ensure_models, run_league


def research_sweep_sync(
    *,
    league_ids: List[str],
    min_samples: int = 40,
    top_n: int = 25,
    train_missing: bool = True,
    progress_cb=None,
) -> Dict[str, Any]:
    reports = []
    total = max(1, len(league_ids))
    for i, lid in enumerate(league_ids):
        if progress_cb:
            progress_cb(i / total, f"Researching {lid}...")
        if train_missing:
            # Expand ensure_models via TRAIN_PLAN already
            ensure_models(lid)
        reports.append(run_league(lid, min_samples, top_n))

    flat = []
    for r in reports:
        flat.extend(r.get("top") or [])
    flat.sort(key=lambda x: x.get("score", 0), reverse=True)

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "min_samples": min_samples,
        "leagues": reports,
        "global_top": flat[:40],
    }
    out_dir = PROJECT_ROOT / "data" / "research"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"sweep-{stamp}.json"
    path.write_text(json.dumps(out, indent=2))
    out["path"] = str(path.relative_to(PROJECT_ROOT))
    if progress_cb:
        progress_cb(1.0, "Research complete")
    return out


def list_research_reports(limit: int = 20) -> List[Dict[str, Any]]:
    out_dir = PROJECT_ROOT / "data" / "research"
    if not out_dir.exists():
        return []
    files = sorted(out_dir.glob("sweep-*.json"), reverse=True)[:limit]
    rows = []
    for f in files:
        try:
            data = json.loads(f.read_text())
            rows.append(
                {
                    "name": f.name,
                    "path": str(f.relative_to(PROJECT_ROOT)),
                    "generated_at": data.get("generated_at"),
                    "leagues": len(data.get("leagues") or []),
                    "top_count": len(data.get("global_top") or []),
                }
            )
        except Exception:
            rows.append({"name": f.name, "path": str(f.relative_to(PROJECT_ROOT)), "error": "unreadable"})
    return rows


def load_research_report(name: str) -> Optional[Dict[str, Any]]:
    path = PROJECT_ROOT / "data" / "research" / Path(name).name
    if not path.exists() or not path.name.startswith("sweep-"):
        return None
    return json.loads(path.read_text())
