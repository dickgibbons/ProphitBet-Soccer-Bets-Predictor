from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from web import db
from web.auth import require_auth
from web.config import app_url
from web.jobs import enqueue
from web.services import evaluate as evaluate_service
from web.services import leagues as league_service
from web.services import models as model_service
from web.templating import templates

router = APIRouter(prefix="/models")


def _train_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return model_service.train_model_sync(
        league_id=payload["league_id"],
        model_id=payload["model_id"],
        model_type=payload["model_type"],
        target_key=payload["target_key"],
        eval_ratio=float(payload.get("eval_ratio", 0.2)),
        normalizer_key=payload.get("normalizer_key", "standard"),
        sampler_key=payload.get("sampler_key", "none"),
        calibrate=bool(payload.get("calibrate", True)),
        run_cv=bool(payload.get("run_cv", False)),
        cv_folds=int(payload.get("cv_folds", 5)),
        sliding_cv=bool(payload.get("sliding_cv", False)),
        tune=bool(payload.get("tune", False)),
        tune_trials=int(payload.get("tune_trials", 20)),
        tune_metric=payload.get("tune_metric", "Accuracy"),
        hyperparams=payload.get("hyperparams") or {},
        progress_cb=progress_cb,
    )


def _batch_train_job(job_id: int, payload: dict) -> dict:
    def progress_cb(progress: float, message: str):
        db.update_job(job_id, progress=progress, message=message)

    return model_service.batch_train_sync(
        league_id=payload["league_id"],
        model_types=payload["model_types"],
        target_keys=payload["target_keys"],
        eval_ratio=float(payload.get("eval_ratio", 0.2)),
        progress_cb=progress_cb,
    )


@router.get("", response_class=HTMLResponse)
def models_manager(request: Request, league_id: str = "", user: str = Depends(require_auth)):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id) if league_id else []
    return templates.TemplateResponse(
        "models/manager.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "selected_league": league_id,
            "model_choices": model_service.available_model_choices(),
            "target_choices": model_service.TARGET_CHOICES,
        },
    )


@router.get("/train", response_class=HTMLResponse)
def train_form(request: Request, league_id: str = "", user: str = Depends(require_auth)):
    return templates.TemplateResponse(
        "models/train.html",
        {
            "request": request,
            "user": user,
            "leagues": league_service.list_created_leagues(),
            "selected_league": league_id,
            "model_choices": model_service.available_model_choices(),
            "target_choices": model_service.TARGET_CHOICES,
            "error": None,
        },
    )


@router.post("/train")
def train_model(
    request: Request,
    league_id: str = Form(...),
    model_id: str = Form(...),
    model_type: str = Form(...),
    target_key: str = Form(...),
    eval_ratio: float = Form(0.2),
    normalizer_key: str = Form("standard"),
    sampler_key: str = Form("none"),
    calibrate: str = Form("yes"),
    run_cv: str = Form(""),
    sliding_cv: str = Form(""),
    cv_folds: int = Form(5),
    tune: str = Form(""),
    tune_trials: int = Form(20),
    tune_metric: str = Form("Accuracy"),
    n_estimators: int = Form(100),
    max_depth: str = Form(""),
    learning_rate: float = Form(0.3),
    n_neighbors: int = Form(5),
    kernel: str = Form("linear"),
    penalty: str = Form("l2"),
    user: str = Depends(require_auth),
):
    hyperparams = {
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "learning_rate": learning_rate,
        "n_neighbors": n_neighbors,
        "kernel": kernel,
        "penalty": penalty,
    }
    payload = {
        "league_id": league_id,
        "model_id": model_id.strip(),
        "model_type": model_type,
        "target_key": target_key,
        "eval_ratio": eval_ratio,
        "normalizer_key": normalizer_key,
        "sampler_key": sampler_key,
        "calibrate": calibrate == "yes",
        "run_cv": run_cv == "on",
        "sliding_cv": sliding_cv == "on",
        "cv_folds": cv_folds,
        "tune": tune == "on",
        "tune_trials": tune_trials,
        "tune_metric": tune_metric,
        "hyperparams": hyperparams,
    }
    try:
        mdb_models = model_service.list_models(league_id)
        if any(m["model_id"] == payload["model_id"] for m in mdb_models):
            raise ValueError(f"Model id already exists: {payload['model_id']}")
        job_id = enqueue("train_model", payload, _train_job, message="Queued training")
        return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)
    except Exception as exc:
        return templates.TemplateResponse(
            "models/train.html",
            {
                "request": request,
                "user": user,
                "leagues": league_service.list_created_leagues(),
                "selected_league": league_id,
                "model_choices": model_service.available_model_choices(),
                "target_choices": model_service.TARGET_CHOICES,
                "error": str(exc),
            },
            status_code=400,
        )


@router.post("/batch-train")
def batch_train(
    league_id: str = Form(...),
    model_types: list[str] = Form(...),
    target_keys: list[str] = Form(...),
    eval_ratio: float = Form(0.2),
    user: str = Depends(require_auth),
):
    if isinstance(model_types, str):
        model_types = [model_types]
    if isinstance(target_keys, str):
        target_keys = [target_keys]
    payload = {
        "league_id": league_id,
        "model_types": model_types,
        "target_keys": target_keys,
        "eval_ratio": eval_ratio,
    }
    job_id = enqueue("batch_train", payload, _batch_train_job, message="Queued batch training")
    return RedirectResponse(app_url(f"/jobs/{job_id}"), status_code=303)


@router.get("/evaluate", response_class=HTMLResponse)
def evaluate_form(request: Request, league_id: str = "", model_id: str = "", user: str = Depends(require_auth)):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id) if league_id else []
    filters = evaluate_service.list_filters(league_id, model_id) if league_id and model_id else []
    return templates.TemplateResponse(
        "models/evaluate.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "selected_league": league_id,
            "selected_model": model_id,
            "odd_ranges": evaluate_service.odd_range_choices(),
            "filters": filters,
            "result": None,
            "error": None,
        },
    )


@router.post("/evaluate", response_class=HTMLResponse)
def evaluate_run(
    request: Request,
    league_id: str = Form(...),
    model_id: str = Form(...),
    dataset: str = Form("Eval"),
    odd_range: str = Form("none"),
    p1: float = Form(0),
    px: float = Form(0),
    p2: float = Form(0),
    pu: float = Form(0),
    po: float = Form(0),
    user: str = Depends(require_auth),
):
    leagues = league_service.list_created_leagues()
    models = model_service.list_models(league_id)
    filters = evaluate_service.list_filters(league_id, model_id)
    try:
        result = evaluate_service.evaluate_model(
            league_id=league_id,
            model_id=model_id,
            dataset=dataset,
            odd_range_key=odd_range,
            percentiles={"p1": p1, "px": px, "p2": p2, "pu": pu, "po": po},
        )
        result.pop("_preview_df", None)
        error = None
    except Exception as exc:
        result = None
        error = str(exc)

    return templates.TemplateResponse(
        "models/evaluate.html",
        {
            "request": request,
            "user": user,
            "leagues": leagues,
            "models": models,
            "selected_league": league_id,
            "selected_model": model_id,
            "odd_ranges": evaluate_service.odd_range_choices(),
            "filters": filters,
            "result": result,
            "error": error,
            "form": {
                "dataset": dataset,
                "odd_range": odd_range,
                "p1": p1,
                "px": px,
                "p2": p2,
                "pu": pu,
                "po": po,
            },
        },
    )


@router.get("/evaluate/export")
def evaluate_export(
    league_id: str,
    model_id: str,
    dataset: str = "Eval",
    odd_range: str = "none",
    p1: float = 0,
    px: float = 0,
    p2: float = 0,
    pu: float = 0,
    po: float = 0,
    fmt: str = "csv",
    user: str = Depends(require_auth),
):
    result = evaluate_service.evaluate_model(
        league_id=league_id,
        model_id=model_id,
        dataset=dataset,
        odd_range_key=odd_range,
        percentiles={"p1": p1, "px": px, "p2": p2, "pu": pu, "po": po},
    )
    preview_df = result.pop("_preview_df")
    data = evaluate_service.export_filtered_preview(preview_df, fmt=fmt)
    media = "text/csv" if fmt == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    filename = f"eval-{league_id}-{model_id}.{fmt}"
    return Response(
        content=data,
        media_type=media,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/evaluate/filter")
def store_filter(
    league_id: str = Form(...),
    model_id: str = Form(...),
    name: str = Form(...),
    dataset: str = Form("Eval"),
    odd_range: str = Form("none"),
    p1: float = Form(0),
    px: float = Form(0),
    p2: float = Form(0),
    pu: float = Form(0),
    po: float = Form(0),
    user: str = Depends(require_auth),
):
    evaluate_service.save_filter(
        league_id,
        model_id,
        name.strip(),
        {
            "dataset": dataset,
            "odd_range": odd_range,
            "percentiles": {"p1": p1, "px": px, "p2": p2, "pu": pu, "po": po},
        },
    )
    return RedirectResponse(
        app_url(f"/models/evaluate?league_id={league_id}&model_id={model_id}"),
        status_code=303,
    )


@router.post("/evaluate/filter/{filter_id}/delete")
def remove_filter(filter_id: int, league_id: str = Form(...), model_id: str = Form(...), user: str = Depends(require_auth)):
    evaluate_service.delete_filter(filter_id)
    return RedirectResponse(
        app_url(f"/models/evaluate?league_id={league_id}&model_id={model_id}"),
        status_code=303,
    )


@router.post("/{league_id}/{model_id}/delete")
def delete_model(league_id: str, model_id: str, user: str = Depends(require_auth)):
    try:
        model_service.delete_model(league_id, model_id)
    except Exception:
        pass
    return RedirectResponse(app_url(f"/models?league_id={league_id}"), status_code=303)
