from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

from web.auth import require_auth
from web.services import explain as explain_service
from web.services import leagues as league_service
from web.services import models as model_service
from web.templating import templates

router = APIRouter(prefix="/explain")


@router.get("", response_class=HTMLResponse)
def explain_form(request: Request, league_id: str = "", model_id: str = "", user: str = Depends(require_auth)):
    models = model_service.list_models(league_id) if league_id else []
    return templates.TemplateResponse(
        "explain/index.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "models": models,
            "selected_league": league_id,
            "selected_model": model_id,
            "result": None,
            "error": None,
        },
    )


@router.post("", response_class=HTMLResponse)
def explain_run(
    request: Request,
    league_id: str = Form(...),
    model_id: str = Form(...),
    plot_type: str = Form("shap_bar"),
    target_label: str = Form(""),
    feature_a: str = Form("1"),
    feature_b: str = Form("X"),
    match_index: int = Form(0),
    user: str = Depends(require_auth),
):
    models = model_service.list_models(league_id)
    hint = ""
    for m in models:
        if m["model_id"] == model_id:
            hint = m.get("model_type") or ""
            break
    try:
        result = explain_service.explain_model(
            league_id=league_id,
            model_id=model_id,
            plot_type=plot_type,
            target_label=target_label or None,
            feature_a=feature_a,
            feature_b=feature_b,
            match_index=match_index,
            model_type_hint=hint,
        )
        error = None
    except Exception as exc:
        result = None
        error = str(exc)
    return templates.TemplateResponse(
        "explain/index.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "models": models,
            "selected_league": league_id,
            "selected_model": model_id,
            "result": result,
            "error": error,
            "form": {
                "plot_type": plot_type,
                "target_label": target_label,
                "feature_a": feature_a,
                "feature_b": feature_b,
                "match_index": match_index,
            },
        },
    )
