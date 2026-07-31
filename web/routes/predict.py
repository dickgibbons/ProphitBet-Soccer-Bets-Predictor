import json
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from web.auth import require_auth
from web.config import app_url
from web.services import fixtures as fixtures_service
from web.services import leagues as league_service
from web.services import models as model_service
from web.services import predict as predict_service
from web.templating import templates

router = APIRouter(prefix="/predict")


@router.get("/fixtures", response_class=HTMLResponse)
def fixtures_form(request: Request, league_id: str = "", user: str = Depends(require_auth)):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id) if league_id else []
    return templates.TemplateResponse(
        "predict/fixtures.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "selected_league": league_id,
            "today": date.today().isoformat(),
            "result": None,
            "error": None,
        },
    )


@router.post("/fixtures", response_class=HTMLResponse)
async def fixtures_predict(
    request: Request,
    league_id: str = Form(...),
    model_id: str = Form(...),
    fixture_date: str = Form(...),
    csv_file: Optional[UploadFile] = File(None),
    user: str = Depends(require_auth),
):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id)
    result = None
    error = None
    try:
        if csv_file is not None and csv_file.filename:
            content = await csv_file.read()
            fixtures = fixtures_service.parse_fixtures_csv(content)
        else:
            fixtures = fixtures_service.scrape_fixtures(league_id, fixture_date)
        result = fixtures_service.predict_fixtures(
            league_id=league_id, model_id=model_id, fixtures=fixtures
        )
        # stash in cookie for export
        request.state.fixtures_rows = result["rows"]
    except Exception as exc:
        error = str(exc)

    response = templates.TemplateResponse(
        "predict/fixtures.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "selected_league": league_id,
            "selected_model": model_id,
            "today": fixture_date or date.today().isoformat(),
            "result": result,
            "error": error,
        },
    )
    if result:
        response.set_cookie(
            "fixtures_history",
            json.dumps(result["rows"])[:3500],
            max_age=60 * 60 * 24,
        )
    return response


@router.get("/fixtures/export")
def fixtures_export(request: Request, fmt: str = "csv", user: str = Depends(require_auth)):
    raw = request.cookies.get("fixtures_history")
    rows = []
    if raw:
        try:
            rows = json.loads(raw)
        except json.JSONDecodeError:
            rows = []
    if not rows:
        return RedirectResponse(app_url("/predict/fixtures"), status_code=302)
    content = fixtures_service.export_fixture_rows(rows, fmt=fmt)
    if fmt == "xlsx":
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=fixtures.xlsx"},
        )
    return Response(
        content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fixtures.csv"},
    )


@router.get("/manual", response_class=HTMLResponse)
def manual_form(request: Request, league_id: str = "", user: str = Depends(require_auth)):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id) if league_id else []
    teams = predict_service.team_options(league_id) if league_id else {"home": [], "away": []}
    history: List[dict] = []
    raw = request.cookies.get("predict_history")
    if raw:
        try:
            history = json.loads(raw)
        except json.JSONDecodeError:
            history = []
    return templates.TemplateResponse(
        "predict/manual.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "teams": teams,
            "selected_league": league_id,
            "result": None,
            "history": history,
            "error": None,
        },
    )


@router.post("/manual", response_class=HTMLResponse)
def manual_predict(
    request: Request,
    league_id: str = Form(...),
    model_id: str = Form(...),
    home: str = Form(...),
    away: str = Form(...),
    odd_1: float = Form(...),
    odd_x: float = Form(...),
    odd_2: float = Form(...),
    user: str = Depends(require_auth),
):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id)
    teams = predict_service.team_options(league_id)
    history: List[dict] = []
    raw = request.cookies.get("predict_history")
    if raw:
        try:
            history = json.loads(raw)
        except json.JSONDecodeError:
            history = []

    try:
        result = predict_service.predict_manual(
            league_id=league_id,
            model_id=model_id,
            home=home,
            away=away,
            odd_1=odd_1,
            odd_x=odd_x,
            odd_2=odd_2,
        )
        history = [result] + history
        history = history[:50]
        error = None
    except Exception as exc:
        result = None
        error = str(exc)

    response = templates.TemplateResponse(
        "predict/manual.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "teams": teams,
            "selected_league": league_id,
            "selected_model": model_id,
            "result": result,
            "history": history,
            "error": error,
        },
    )
    response.set_cookie("predict_history", json.dumps(history), max_age=60 * 60 * 24 * 7)
    return response


@router.get("/export")
def export_history(request: Request, fmt: str = "csv", user: str = Depends(require_auth)):
    history: List[dict] = []
    raw = request.cookies.get("predict_history")
    if raw:
        try:
            history = json.loads(raw)
        except json.JSONDecodeError:
            history = []
    if not history:
        return RedirectResponse(app_url("/predict/manual"), status_code=302)

    content = predict_service.export_predictions(history, fmt=fmt)
    if fmt == "xlsx":
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=predictions.xlsx"},
        )
    return Response(
        content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"},
    )
