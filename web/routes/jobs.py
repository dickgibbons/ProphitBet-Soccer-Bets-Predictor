from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from web import db
from web.auth import require_auth
from web.config import app_url
from web.jobs import job_view
from web.templating import templates

router = APIRouter(prefix="/jobs")


@router.get("", response_class=HTMLResponse)
def jobs_list(request: Request, user: str = Depends(require_auth)):
    return templates.TemplateResponse(
        "jobs/list.html",
        {"request": request, "user": user, "jobs": db.list_jobs(limit=100)},
    )


@router.get("/{job_id}", response_class=HTMLResponse)
def job_detail(job_id: int, request: Request, user: str = Depends(require_auth)):
    job = job_view(job_id)
    if not job:
        return RedirectResponse(app_url("/"), status_code=302)
    return templates.TemplateResponse(
        "jobs/detail.html",
        {"request": request, "user": user, "job": job},
    )


@router.get("/{job_id}/status", response_class=HTMLResponse)
def job_status_partial(job_id: int, request: Request, user: str = Depends(require_auth)):
    job = job_view(job_id)
    if not job:
        return HTMLResponse("<div class='error'>Job not found</div>", status_code=404)
    return templates.TemplateResponse(
        "jobs/status_partial.html",
        {"request": request, "job": job},
    )
