from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from web import db
from web.auth import require_auth
from web.config import app_url
from web.jobs import enqueue
from web.services import leagues as league_service
from web.services import research as research_service
from web.templating import templates

router = APIRouter(prefix="/research")


def _research_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return research_service.research_sweep_sync(
        league_ids=payload["league_ids"],
        min_samples=int(payload.get("min_samples", 40)),
        top_n=int(payload.get("top_n", 25)),
        train_missing=bool(payload.get("train_missing", True)),
        progress_cb=progress_cb,
    )


@router.get("", response_class=HTMLResponse)
def research_home(request: Request, report: str = "", user: str = Depends(require_auth)):
    data = research_service.load_research_report(report) if report else None
    return templates.TemplateResponse(
        "research/index.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "reports": research_service.list_research_reports(),
            "selected_report": report,
            "report_data": data,
        },
    )


@router.post("/run")
def research_run(
    league_ids: list[str] = Form(...),
    min_samples: int = Form(40),
    top_n: int = Form(25),
    train_missing: str = Form("on"),
    user: str = Depends(require_auth),
):
    if isinstance(league_ids, str):
        league_ids = [league_ids]
    payload = {
        "league_ids": league_ids,
        "min_samples": min_samples,
        "top_n": top_n,
        "train_missing": train_missing == "on",
    }
    job_id = enqueue("research_sweep", payload, _research_job, message="Queued research sweep")
    return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)
