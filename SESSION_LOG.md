# SESSION_LOG

## 2026-07-31 — Synced to GitHub fork

- Committed web app, research scripts, PLAYBOOK, deploy docs (70 files).
- Pushed to https://github.com/dickgibbons/ProphitBet-Soccer-Bets-Predictor (`fork` remote). Did not push to upstream `kochlisGit`.
- League data / trained models / sweep JSON stay on VPS only (`data/` gitignored).

## 2026-07-31 — Predict dropdown missing new leagues

- Cause: uvicorn kept in-memory `LeagueDatabase` from startup; batch created 28 leagues on disk but UI still showed old top-5 set.
- Fix: restarted `prophitbet-web`; `list_created_leagues()` now calls `refresh_league_db()` so disk updates show without restart. Deployed to VPS.

## 2026-07-31 — Healthy ROI playbook

- Built `PLAYBOOK.md` + `data/research/playbook-healthy.json` from `sweep-live.json` + `sweep-all-new.json`.
- Criteria: Eval ROI > 20%, n ≥ 40; deduped to best per league+model+odds band (94 edges, 26 leagues).
- Tiers: A n≥80 (6), B n≥60 (22), C n≥50 (18), D n40–49 (48). Synced copies to VPS `data/research/`.

## 2026-07-31 — Batch create + research all remaining leagues

- User `go`: create all 28 football-data leagues not already researched (skip top-5 EPL/La Liga/Serie A/Ligue 1/Bundesliga), then research-sweep.
- Fixed broken VPS script (`batch_all_leagues.py` SyntaxError from SSH heredoc eating quotes); redeployed via rsync + `docker cp`.
- Completed: 28 created, 28 researched, 0 script errors; MLS 0 candidates (odds `'x'` broke training).
- Output: `data/research/sweep-all-new.json` (top 50). Strong themes: China Super League away 1.91–2.5 (lr), Argentina away 1.91–2.5 (rf), Allsvenskan draw band (xgb), Brazil Serie A away 2.5–3.5 (xgb).
- 20-min progress loop stopped after finish.

## 2026-07-30 — Live research refresh

- Ran `research_sweep.py` on EPL + La Liga/Serie A/Ligue 1/Bundesliga `-02` leagues; trained new targets (BTTS, O/U 1.5/3.5, DT/SVM).
- Results: `data/research/sweep-live.json` on VPS; playbook themes unchanged (EPL away 2.5–3.5, Serie A away 1.91–2.5, La Liga home dogs 2.5–3.5; Bundesliga skip).

## 2026-07-30 — Full web buildout (Waves 1–3)

- Wave 1: all sklearn classifiers, train knobs (normalizer/sampler/calibration/CV/Optuna), BTTS + O/U 1.5/3.5, model manager + batch train, seasonal eval export, league update/bulk, in-app Research page.
- Wave 2: Fixtures page (Selenium scrape + CSV fallback), Analysis + Explain pages (lazy deps).
- Wave 3: optional NeuralNetwork in MODEL_TYPES when TF present; Docker targets slim/analysis/fixtures/full-ml.
- Docs: USER_GUIDE.md + DEPLOY.md updated for profiles.

## 2026-07-30 — Automated research sweep

- Added `scripts/research_sweep.py`: trains LR/RF/XGB (Result + O/U), grids odd bands × probability percentiles on Eval, ranks by unit-stake ROI + Profit Balance.
- Ran on VPS for EPL + created La Liga / Serie A / Bundesliga / Ligue 1 (2018+, history=3, margin=2).
- Saved strongest Eval filters into app DB; results in `data/research_*.json` + canvas `prophitbet-research`.
- Themes: mid-price away (≈1.9–3.5) and some soft home bands; Bundesliga near-flat — skip.

## 2026-07-30 — User guide in app

- Added `USER_GUIDE.md` covering workflow, field meanings, and when to change knobs.
- Wired `/guide` into the web nav/home; Dockerfile copies the markdown into the image.

## 2026-07-30 — VPS hub tile (live)

- Deployed to VPS: app at `/root/dashboard/prophitbet` (Docker `prophitbet-web`, `127.0.0.1:8010`).
- Hub tiles synced to `/root/dashboard/Agents/frontend/{index,sports-betting}.html`.
- Nginx: `https://gibbonsai.com/prophitbet/` → `:8010` (`ROOT_PATH=/prophitbet`).
- Made `src/models/classifiers/__init__.py` tolerate missing TensorFlow for the slim web image.

## 2026-07-30 — ProphitBet Web MVP

- Built FastAPI + HTMX web MVP under `web/` with SQLite jobs/filters, basic auth, Docker Compose.
- Reuses `src/` league downloaders, stats, LR/RF/XGB trainers, metrics; no TF/Selenium/PyQt in `requirements-web.txt`.
- Verified locally: pages 200 OK; train/eval/predict + CSV/XLSX export on existing EPL data; job queue works.
- Deploy notes in `DEPLOY.md`; launch via `./run_web.sh` or `docker compose up -d --build`.

## 2026-07-30 — Blank launch window

- User saw empty white ProphitBet window on first launch; menus were present.
- Root cause: by design, no central widget until a league is created/loaded (`centralWidget()` was `None`).
- Fix: apply default qdarktheme on startup + empty-state placeholder instructing File → New League; welcome dialog updated with same hint.

## 2026-07-30 — Install & explore ProphitBet

- Cloned [kochlisGit/ProphitBet-Soccer-Bets-Predictor](https://github.com/kochlisGit/ProphitBet-Soccer-Bets-Predictor) into `/Users/dickgibbons/AI Projects/sports-betting/ProphitBet-Soccer-Bets-Predictor`.
- Created Python 3.11 venv (`.venv`) and installed pinned deps from `requirements.txt`.
- macOS Apple Silicon note: `tensorflow-io-gcs-filesystem==0.31.0` has no arm64 wheel; used `0.37.1` instead. Rest of stack (TF 2.15.1, PyQt6, sklearn, xgboost) imports cleanly.
- Fixed `install.py` docstring (`r"""..."""`) so Windows `\Users` paths don't raise `SyntaxError` on import/run.
- Smoke-checked: `MainWindow` import OK; created `run_app.sh` to launch with venv.
- App overview: PyQt6 desktop GUI (ProphitBet-v2). Data from football-data.co.uk + Footystats fixtures. Modules under `src/`: analysis, database, gui, interpretability, metrics, models, network, preprocessing.
