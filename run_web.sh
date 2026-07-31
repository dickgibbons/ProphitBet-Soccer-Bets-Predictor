#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH=.
export PROPHITBET_USER="${PROPHITBET_USER:-admin}"
export PROPHITBET_PASSWORD="${PROPHITBET_PASSWORD:-changeme}"
# Uncomment for local no-auth testing:
# export PROPHITBET_AUTH_DISABLED=1
exec uvicorn web.app:app --host 0.0.0.0 --port "${PORT:-8010}" "$@"
