from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

from web.auth import require_auth
from web.services import analysis as analysis_service
from web.services import leagues as league_service
from web.services import models as model_service
from web.templating import templates

router = APIRouter(prefix="/analysis")


@router.get("", response_class=HTMLResponse)
def analysis_form(request: Request, league_id: str = "", user: str = Depends(require_auth)):
    return templates.TemplateResponse(
        "analysis/index.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "selected_league": league_id,
            "analysis_types": analysis_service.ANALYSIS_TYPES,
            "target_choices": model_service.TARGET_CHOICES,
            "result": None,
            "error": None,
        },
    )


@router.post("", response_class=HTMLResponse)
def analysis_run(
    request: Request,
    league_id: str = Form(...),
    analysis_type: str = Form(...),
    season: str = Form(""),
    target_key: str = Form("result"),
    colormap: str = Form("Blues"),
    user: str = Depends(require_auth),
):
    season_val: Optional[int] = int(season) if season.strip() else None
    try:
        result = analysis_service.run_analysis(
            league_id=league_id,
            analysis_type=analysis_type,
            season=season_val,
            target_key=target_key,
            colormap=colormap,
        )
        error = None
    except Exception as exc:
        result = None
        error = str(exc)
    return templates.TemplateResponse(
        "analysis/index.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "selected_league": league_id,
            "analysis_types": analysis_service.ANALYSIS_TYPES,
            "target_choices": model_service.TARGET_CHOICES,
            "result": result,
            "error": error,
            "form": {
                "analysis_type": analysis_type,
                "season": season,
                "target_key": target_key,
                "colormap": colormap,
            },
        },
    )
