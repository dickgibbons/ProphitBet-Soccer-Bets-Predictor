# Default slim image: train/eval/research (no Selenium / TensorFlow).
# Profiles:
#   docker compose --profile fixtures build
#   docker compose --profile full-ml build
ARG REQUIREMENTS_FILE=requirements-web.txt

FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PROPHITBET_USER=admin \
    PROPHITBET_PASSWORD=changeme \
    DATABASE_URL=sqlite:///data/app.db \
    FOOTYSTATS_HEADLESS=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ARG REQUIREMENTS_FILE
COPY requirements-web.txt requirements-fixtures.txt requirements-analysis.txt requirements-full-ml.txt ./
RUN pip install -r ${REQUIREMENTS_FILE}

COPY src ./src
COPY storage ./storage
COPY web ./web
COPY scripts ./scripts
COPY USER_GUIDE.md ./USER_GUIDE.md

RUN mkdir -p /app/data /app/storage/leagues /app/data/research

EXPOSE 8000
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]

# Fixtures profile: Chromium + Selenium
FROM base AS fixtures
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*
ENV CHROME_BIN=/usr/bin/chromium \
    FOOTYSTATS_HEADLESS=1

# Full ML: same as fixtures base packages already installed via REQUIREMENTS_FILE
FROM fixtures AS full-ml
