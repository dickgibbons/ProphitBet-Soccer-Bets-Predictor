from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from web import db
from web.auth import require_auth
from web.config import app_url
from web.templating import templates
from web.jobs import enqueue
from web.services import leagues as league_service
from web.services import models as model_service

router = APIRouter(prefix="/leagues")
def _create_league_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return league_service.create_league_sync(
        template_index=int(payload["template_index"]),
        league_id=payload["league_id"],
        start_year=int(payload["start_year"]),
        match_history_window=int(payload.get("match_history_window", 3)),
        goal_diff_margin=int(payload.get("goal_diff_margin", 2)),
        progress_cb=progress_cb,
    )


@router.get("", response_class=HTMLResponse)
def leagues_list(request: Request, user: str = Depends(require_auth)):
    return templates.TemplateResponse(
        "leagues/list.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
        },
    )


@router.get("/new", response_class=HTMLResponse)
def new_league_form(request: Request, user: str = Depends(require_auth)):
    templates_list = league_service.available_league_templates()
    return templates.TemplateResponse(
        "leagues/new.html",
        {
            "request": request,
            "user": user,
            "templates": templates_list,
            "default_start_year": max(2015, date.today().year - 8),
            "error": None,
        },
    )


@router.post("/new")
def create_league(
    request: Request,
    template_index: int = Form(...),
    league_id: str = Form(""),
    start_year: int = Form(...),
    match_history_window: int = Form(3),
    goal_diff_margin: int = Form(2),
    user: str = Depends(require_auth),
):
    templates_list = league_service.available_league_templates()
    league_id = (league_id or "").strip()
    if not league_id:
        # Server-side fallback if the browser left it blank.
        tpl = next((t for t in templates_list if t["index"] == template_index), None)
        if tpl is None:
            raise ValueError("Invalid league selection.")
        league_id = league_service.suggest_league_id(tpl["name"], tpl["country"])

    payload = {
        "template_index": template_index,
        "league_id": league_id,
        "start_year": start_year,
        "match_history_window": match_history_window,
        "goal_diff_margin": goal_diff_margin,
    }
    try:
        ldb = league_service.get_league_db()
        if ldb.league_exists(payload["league_id"]):
            raise ValueError(f"League id already exists: {payload['league_id']}")
        job_id = enqueue(
            "create_league",
            payload,
            _create_league_job,
            message="Queued league download",
        )
        return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)
    except Exception as exc:
        return templates.TemplateResponse(
            "leagues/new.html",
            {
                "request": request,
                "user": user,
                "templates": templates_list,
                "selected_template": template_index,
                "default_start_year": start_year,
                "error": str(exc),
            },
            status_code=400,
        )


@router.get("/{league_id}", response_class=HTMLResponse)
def league_detail(
    league_id: str,
    request: Request,
    q: str = "",
    hide_missing: bool = False,
    user: str = Depends(require_auth),
):
    league = league_service.get_league(league_id)
    df = league_service.load_league_frame(league_id)
    if league is None or df is None:
        return RedirectResponse(app_url("/leagues"), status_code=302)

    filtered = league_service.filter_matches(df, query=q, hide_missing=hide_missing)
    records = league_service.dataframe_to_records(filtered, limit=300)
    columns = list(filtered.columns) if not filtered.empty else list(df.columns)

    return templates.TemplateResponse(
        "leagues/detail.html",
        {
            "request": request,
            "user": user,
            "league": league,
            "league_id": league_id,
            "columns": columns,
            "rows": records,
            "total_rows": int(df.shape[0]),
            "shown_rows": len(records),
            "filtered_rows": int(filtered.shape[0]),
            "q": q,
            "hide_missing": hide_missing,
            "models": model_service.list_models(league_id),
        },
    )


@router.get("/{league_id}/table", response_class=HTMLResponse)
def league_table_partial(
    league_id: str,
    request: Request,
    q: str = "",
    hide_missing: bool = False,
    user: str = Depends(require_auth),
):
    df = league_service.load_league_frame(league_id)
    if df is None:
        return HTMLResponse("<div class='error'>League not found</div>", status_code=404)
    filtered = league_service.filter_matches(df, query=q, hide_missing=hide_missing)
    records = league_service.dataframe_to_records(filtered, limit=300)
    columns = list(filtered.columns) if not filtered.empty else list(df.columns)
    return templates.TemplateResponse(
        "leagues/table_partial.html",
        {
            "request": request,
            "columns": columns,
            "rows": records,
            "filtered_rows": int(filtered.shape[0]),
            "shown_rows": len(records),
        },
    )


def _update_league_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return league_service.update_league_sync(payload["league_id"], progress_cb=progress_cb)


def _bulk_create_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return league_service.bulk_create_leagues_sync(specs=payload["specs"], progress_cb=progress_cb)


@router.post("/{league_id}/update")
def update_league(league_id: str, user: str = Depends(require_auth)):
    job_id = enqueue(
        "update_league",
        {"league_id": league_id},
        _update_league_job,
        message="Queued league update",
    )
    return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)


@router.post("/bulk")
def bulk_create(
    template_indices: list[int] = Form(...),
    start_year: int = Form(2018),
    user: str = Depends(require_auth),
):
    if isinstance(template_indices, int):
        template_indices = [template_indices]
    specs = [{"template_index": int(i), "start_year": start_year} for i in template_indices]
    job_id = enqueue("bulk_create_leagues", {"specs": specs}, _bulk_create_job, message="Queued bulk league create")
    return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)


@router.post("/{league_id}/delete")
def delete_league(league_id: str, user: str = Depends(require_auth)):
    try:
        league_service.delete_league(league_id)
    except Exception:
        pass
    return RedirectResponse(app_url("/leagues"), status_code=303)
