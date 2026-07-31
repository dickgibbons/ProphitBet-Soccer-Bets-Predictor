# ProphitBet Web — VPS Deploy

FastAPI + HTMX app with modular Docker images.

## Profiles

| Build | Env | Includes |
|-------|-----|----------|
| **slim (default)** | `REQUIREMENTS_FILE=requirements-web.txt` `DOCKER_TARGET=base` | Leagues, all sklearn models, Optuna/CV, bet types, research, manual predict |
| **analysis** | `REQUIREMENTS_FILE=requirements-analysis.txt` `DOCKER_TARGET=base` | + SHAP, Boruta, analysis/explain pages |
| **fixtures** | `REQUIREMENTS_FILE=requirements-fixtures.txt` `DOCKER_TARGET=fixtures` | + Chromium/Selenium FootyStats scrape |
| **full-ml** | `REQUIREMENTS_FILE=requirements-full-ml.txt` `DOCKER_TARGET=full-ml` | analysis + fixtures + TensorFlow DNN |

## Quick start (slim)

```bash
cd ProphitBet-Soccer-Bets-Predictor
export PROPHITBET_USER=dick
export PROPHITBET_PASSWORD='use-a-long-password'
docker compose up -d --build
```

Open `https://gibbonsai.com/prophitbet/` (or `http://HOST:8010`).

## Rebuild for a heavier profile

```bash
# Analysis + SHAP / Boruta
REQUIREMENTS_FILE=requirements-analysis.txt DOCKER_TARGET=base \
  docker compose up -d --build

# Fixtures scrape
REQUIREMENTS_FILE=requirements-fixtures.txt DOCKER_TARGET=fixtures \
  docker compose up -d --build

# Everything
REQUIREMENTS_FILE=requirements-full-ml.txt DOCKER_TARGET=full-ml \
  docker compose up -d --build
```

## Data persistence

| Host path | Purpose |
|-----------|---------|
| `./data` | SQLite + research JSON under `data/research/` |
| `./storage/leagues` | League CSVs + model pickles |

## Local run without Docker

```bash
python3.11 -m venv .venv-web
source .venv-web/bin/activate
pip install -r requirements-web.txt
# optional: pip install -r requirements-analysis.txt
export PROPHITBET_AUTH_DISABLED=1
export PYTHONPATH=.
uvicorn web.app:app --reload --port 8000
```

## Workflow

1. **New League** / bulk create / **Update league data**
2. **Models** — batch train or single train (knobs, Optuna, CV)
3. **Evaluate** — filters, seasonal metrics, export
4. **Research** — multi-league filter sweep job
5. **Fixtures** (fixtures profile) or CSV upload / **Predict** manual
6. **Analysis** / **Explain** (analysis or full-ml profile)

## Security

- Change default `changeme` password before public exposure
- Prefer HTTPS reverse proxy; app supports `ROOT_PATH=/prophitbet` and `PROPHITBET_AUTH_DISABLED=1` behind hub auth
