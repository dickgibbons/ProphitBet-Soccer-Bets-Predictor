import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.config import PROJECT_ROOT
from web.db import init_db
from web.routes import api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title="ProphitBet Web", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "web" / "static")), name="static")
app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    init_db()
