from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

import pandas as pd

from src.database.model import ModelDatabase
from src.models.classifiers.decisiontree import DecisionTree
from src.models.classifiers.discriminant import DiscriminantAnalysisClassifier
from src.models.classifiers.extremeboosting import XGBoost
from src.models.classifiers.knn import KNN
from src.models.classifiers.logistic import LogisticRegressor
from src.models.classifiers.naivebayes import NaiveBayes
from src.models.classifiers.randomforest import RandomForest
from src.models.classifiers.svm import SVM
from src.models.model import ClassificationModel
from src.models.trainer import Trainer
from src.models.tuner import Tuner
from src.preprocessing.selection import train_test_split
from src.preprocessing.utils.normalization import NormalizerType
from src.preprocessing.utils.sampling import SamplerType
from src.preprocessing.utils.target import TargetType
from web import db as web_db
from web.services.leagues import load_league_frame

MODEL_TYPES: Dict[str, Type[ClassificationModel]] = {
    "logistic": LogisticRegressor,
    "discriminant": DiscriminantAnalysisClassifier,
    "decision_tree": DecisionTree,
    "random_forest": RandomForest,
    "xgboost": XGBoost,
    "knn": KNN,
    "naive_bayes": NaiveBayes,
    "svm": SVM,
}

# Optional DNN — only when TensorFlow is installed (full-ml profile).
try:
    from src.models.classifiers.neuralnets.nn import NeuralNetwork

    MODEL_TYPES["neural_network"] = NeuralNetwork
except Exception:
    NeuralNetwork = None  # type: ignore

TARGET_TYPES = {
    "result": TargetType.RESULT,
    "over_under": TargetType.OVER_UNDER,
    "over_under_15": TargetType.OVER_UNDER_15,
    "over_under_35": TargetType.OVER_UNDER_35,
    "btts": TargetType.BTTS,
}

NORMALIZERS = {
    "none": None,
    "standard": NormalizerType.STANDARD,
    "min_max": NormalizerType.MIN_MAX,
    "max_abs": NormalizerType.MAX_ABS,
}

SAMPLERS = {
    "none": None,
    "svm_smote": SamplerType.SVM_SMOTE,
    "nearmiss": SamplerType.NEARMISS,
    "instance_hardness": SamplerType.INSTANCE_HARDNESS_THRESHOLD,
}

NO_CALIBRATION = {"discriminant", "neural_network"}

MODEL_CHOICES = [
    {"value": "logistic", "label": "Logistic Regression"},
    {"value": "discriminant", "label": "Discriminant (LDA/QDA)"},
    {"value": "decision_tree", "label": "Decision Tree"},
    {"value": "random_forest", "label": "Random Forest"},
    {"value": "xgboost", "label": "XGBoost"},
    {"value": "knn", "label": "K-Nearest Neighbors"},
    {"value": "naive_bayes", "label": "Naive Bayes"},
    {"value": "svm", "label": "SVM"},
]

TARGET_CHOICES = [
    {"value": "result", "label": "Result (1/X/2)"},
    {"value": "over_under", "label": "Over/Under 2.5"},
    {"value": "over_under_15", "label": "Over/Under 1.5"},
    {"value": "over_under_35", "label": "Over/Under 3.5"},
    {"value": "btts", "label": "BTTS (Yes/No)"},
]

DEFAULT_TUNABLE = {
    "logistic": {"penalty": ["l1", "l2"]},
    "discriminant": {"decision_boundary": ["linear", "quadratic"], "oas": [True, False]},
    "decision_tree": {
        "max_depth": {"low": 2, "high": 20, "step": 1},
        "min_samples_leaf": {"low": 1, "high": 20, "step": 1},
    },
    "random_forest": {
        "n_estimators": {"low": 50, "high": 300, "step": 50},
        "max_depth": {"low": 3, "high": 30, "step": 1},
    },
    "xgboost": {
        "n_estimators": {"low": 50, "high": 300, "step": 50},
        "max_depth": {"low": 2, "high": 10, "step": 1},
        "learning_rate": {"low": 0.05, "high": 0.4, "step": 0.05},
    },
    "knn": {"n_neighbors": {"low": 3, "high": 25, "step": 2}},
    "naive_bayes": {"algorithm": ["gaussian", "complement"]},
    "svm": {"kernel": ["linear", "rbf"], "gamma": {"low": 0.01, "high": 1.0, "step": 0.01}},
}


def available_model_choices() -> List[Dict[str, str]]:
    choices = list(MODEL_CHOICES)
    if "neural_network" in MODEL_TYPES:
        choices.append({"value": "neural_network", "label": "Deep Neural Network"})
    return choices


def list_models(league_id: str) -> List[Dict[str, Any]]:
    meta = {m["model_id"]: m for m in web_db.list_model_meta(league_id)}
    mdb = ModelDatabase(league_id=league_id)
    rows = []
    for model_id in mdb.get_model_ids():
        cfg = mdb.load_model_config(model_id=model_id) or {}
        info = meta.get(model_id, {})
        target = cfg.get("target_type", info.get("target_type"))
        target_value = target.value if isinstance(target, TargetType) else str(target)
        rows.append(
            {
                "model_id": model_id,
                "model_type": info.get("model_type") or cfg.get("cls", type(None)).__name__,
                "target_type": target_value,
                "metrics": info.get("metrics", {}),
                "created_at": info.get("created_at"),
            }
        )
    return rows


def delete_model(league_id: str, model_id: str) -> None:
    mdb = ModelDatabase(league_id=league_id)
    if not mdb.model_exists(model_id):
        raise ValueError(f"Unknown model: {model_id}")
    mdb.delete_model(model_id=model_id)
    web_db.delete_model_meta(league_id, model_id)


def _parse_optional_int(value: Any) -> Optional[int]:
    if value is None or value == "" or value == "none":
        return None
    try:
        iv = int(value)
        return None if iv == 0 else iv
    except (TypeError, ValueError):
        return None


def _build_model(
    *,
    model_type: str,
    league_id: str,
    model_id: str,
    target_type: TargetType,
    normalizer_key: str = "standard",
    sampler_key: str = "none",
    calibrate: bool = True,
    hyperparams: Optional[Dict[str, Any]] = None,
) -> ClassificationModel:
    if model_type not in MODEL_TYPES:
        raise ValueError(f"Unsupported model type: {model_type}")
    hp = dict(hyperparams or {})
    normalizer = NORMALIZERS.get(normalizer_key, NormalizerType.STANDARD)
    sampler = SAMPLERS.get(sampler_key)
    calibrate = False if model_type in NO_CALIBRATION else bool(calibrate)

    common = dict(
        league_id=league_id,
        model_id=model_id,
        target_type=target_type,
        normalizer=normalizer,
        sampler=sampler,
    )

    if model_type == "logistic":
        return LogisticRegressor(
            penalty=hp.get("penalty", "l2"),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "discriminant":
        return DiscriminantAnalysisClassifier(
            oas=bool(hp.get("oas", False)),
            decision_boundary=hp.get("decision_boundary", "linear"),
            **common,
        )
    if model_type == "decision_tree":
        return DecisionTree(
            criterion=hp.get("criterion", "gini"),
            min_samples_leaf=int(hp.get("min_samples_leaf", 1)),
            min_samples_split=int(hp.get("min_samples_split", 2)),
            max_features=hp.get("max_features") or None,
            max_depth=_parse_optional_int(hp.get("max_depth")),
            class_weight=bool(hp.get("class_weight", True)),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "random_forest":
        return RandomForest(
            n_estimators=int(hp.get("n_estimators", 100)),
            criterion=hp.get("criterion", "gini"),
            min_samples_leaf=int(hp.get("min_samples_leaf", 1)),
            min_samples_split=int(hp.get("min_samples_split", 2)),
            max_features=hp.get("max_features", "sqrt"),
            max_depth=_parse_optional_int(hp.get("max_depth")),
            class_weight=bool(hp.get("class_weight", True)),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "xgboost":
        return XGBoost(
            n_estimators=int(hp.get("n_estimators", 100)),
            max_depth=int(hp.get("max_depth", 6)),
            min_child_weight=int(hp.get("min_child_weight", 1)),
            learning_rate=float(hp.get("learning_rate", 0.3)),
            lambda_regularization=float(hp.get("lambda_regularization", 1.0)),
            alpha_regularization=float(hp.get("alpha_regularization", 0.0)),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "knn":
        return KNN(
            n_neighbors=int(hp.get("n_neighbors", 5)),
            weights=hp.get("weights", "uniform"),
            p=int(hp.get("p", 2)),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "naive_bayes":
        return NaiveBayes(
            algorithm=hp.get("algorithm", "gaussian"),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "svm":
        return SVM(
            kernel=hp.get("kernel", "linear"),
            degree=int(hp.get("degree", 3)),
            gamma=float(hp.get("gamma", 1.0)),
            class_weight=bool(hp.get("class_weight", True)),
            calibrate_probabilities=calibrate,
            **common,
        )
    if model_type == "neural_network":
        return NeuralNetwork(
            hidden_layers=int(hp.get("hidden_layers", 2)),
            hidden_units=int(hp.get("hidden_units", 64)),
            dropout_rate=float(hp.get("dropout_rate", 0.1)),
            batch_size=int(hp.get("batch_size", 32)),
            epochs=int(hp.get("epochs", 50)),
            **common,
        )
    raise ValueError(f"Unsupported model type: {model_type}")


def train_model_sync(
    *,
    league_id: str,
    model_id: str,
    model_type: str,
    target_key: str,
    eval_ratio: float = 0.2,
    normalizer_key: str = "standard",
    sampler_key: str = "none",
    calibrate: bool = True,
    run_cv: bool = False,
    cv_folds: int = 5,
    sliding_cv: bool = False,
    tune: bool = False,
    tune_trials: int = 20,
    tune_metric: str = "Accuracy",
    hyperparams: Optional[Dict[str, Any]] = None,
    progress_cb=None,
) -> Dict[str, Any]:
    model_id = model_id.strip()
    if not model_id:
        raise ValueError("Model id is required.")
    if model_type not in MODEL_TYPES:
        raise ValueError(f"Unsupported model type: {model_type}")
    if target_key not in TARGET_TYPES:
        raise ValueError(f"Unsupported target: {target_key}")

    df = load_league_frame(league_id)
    if df is None or df.empty:
        raise ValueError(f"No data for league: {league_id}")

    clean = df.dropna().reset_index(drop=True)
    if clean.shape[0] < 50:
        raise ValueError("Need at least 50 complete rows to train.")

    mdb = ModelDatabase(league_id=league_id)
    if mdb.model_exists(model_id):
        raise ValueError(f"Model id already exists: {model_id}")

    eval_ratio = max(0.05, min(0.4, float(eval_ratio)))
    target_type = TARGET_TYPES[target_key]
    hyperparams = dict(hyperparams or {})

    if progress_cb:
        progress_cb(0.1, "Preparing data...")

    test_size = max(10, int(clean.shape[0] * eval_ratio))
    train_df, eval_df = train_test_split(df=clean, test_size=test_size)

    tune_rows = None
    best_params = None
    if tune:
        if progress_cb:
            progress_cb(0.2, f"Optuna tuning ({tune_trials} trials)...")
        tunable = DEFAULT_TUNABLE.get(model_type, {})
        if not tunable:
            raise ValueError(f"No default tunable params for {model_type}")
        fixed = dict(
            league_id=league_id,
            model_id=f"{model_id}-tune",
            target_type=target_type,
            normalizer=NORMALIZERS.get(normalizer_key, NormalizerType.STANDARD),
            sampler=SAMPLERS.get(sampler_key),
        )
        if model_type not in NO_CALIBRATION:
            fixed["calibrate_probabilities"] = bool(calibrate)
        # Merge non-tuned hyperparams into fixed
        for k, v in hyperparams.items():
            if k not in tunable:
                fixed[k] = v
        tuner = Tuner(
            model_cls=MODEL_TYPES[model_type],
            fixed_params=fixed,
            tunable_params=tunable,
            df=train_df,
            metric=tune_metric,
        )
        study = tuner.tune(trials=int(tune_trials))
        best_params = dict(study.best_params)
        hyperparams.update(best_params)
        tune_rows = [
            {"number": t.number, "value": t.value, **t.params}
            for t in study.trials
            if t.value is not None
        ]

    if progress_cb:
        progress_cb(0.45, f"Training {model_type}...")

    model = _build_model(
        model_type=model_type,
        league_id=league_id,
        model_id=model_id,
        target_type=target_type,
        normalizer_key=normalizer_key,
        sampler_key=sampler_key,
        calibrate=calibrate,
        hyperparams=hyperparams,
    )

    trainer = Trainer()
    model, metrics_df = trainer.train(model=model, train_df=train_df, eval_df=eval_df)

    cv_metrics = None
    if run_cv:
        if progress_cb:
            progress_cb(0.7, "Running K-fold CV...")
        # Rebuild fresh model for CV
        cv_model = _build_model(
            model_type=model_type,
            league_id=league_id,
            model_id=f"{model_id}-cv",
            target_type=target_type,
            normalizer_key=normalizer_key,
            sampler_key=sampler_key,
            calibrate=calibrate,
            hyperparams=hyperparams,
        )
        cv_df = trainer.cross_validation(model=cv_model, df=clean, k_folds=int(cv_folds))
        cv_metrics = cv_df.to_dict(orient="records")

    sliding_metrics = None
    if sliding_cv:
        if progress_cb:
            progress_cb(0.8, "Running sliding CV...")
        slide_model = _build_model(
            model_type=model_type,
            league_id=league_id,
            model_id=f"{model_id}-scv",
            target_type=target_type,
            normalizer_key=normalizer_key,
            sampler_key=sampler_key,
            calibrate=calibrate,
            hyperparams=hyperparams,
        )
        scv_df = trainer.sliding_cross_validation(
            model=slide_model, df=clean, test_ratio=eval_ratio, k_folds=int(cv_folds)
        )
        sliding_metrics = scv_df.to_dict(orient="records")

    if progress_cb:
        progress_cb(0.9, "Saving model...")

    config = model.get_default_model_config()
    config["num_eval_samples"] = int(eval_df.shape[0])
    config["num_train_samples"] = int(train_df.shape[0])
    config["web_train"] = {
        "normalizer": normalizer_key,
        "sampler": sampler_key,
        "calibrate": calibrate,
        "eval_ratio": eval_ratio,
        "hyperparams": hyperparams,
        "best_params": best_params,
    }
    mdb.save_model(model=model, model_config=config)

    metrics = metrics_df.to_dict(orient="records")
    meta_metrics = {
        "rows": metrics,
        "train_samples": train_df.shape[0],
        "eval_samples": eval_df.shape[0],
        "cv": cv_metrics,
        "sliding_cv": sliding_metrics,
        "tune": tune_rows,
        "best_params": best_params,
    }
    web_db.upsert_model_meta(
        league_id=league_id,
        model_id=model_id,
        model_type=model_type,
        target_type=target_type.value,
        metrics=meta_metrics,
    )

    return {
        "league_id": league_id,
        "model_id": model_id,
        "model_type": model_type,
        "target_type": target_type.value,
        "metrics": metrics,
        "train_samples": int(train_df.shape[0]),
        "eval_samples": int(eval_df.shape[0]),
        "best_params": best_params,
        "cv_folds": int(cv_folds) if run_cv else None,
        "tuned": bool(tune),
    }


def batch_train_sync(
    *,
    league_id: str,
    model_types: List[str],
    target_keys: List[str],
    eval_ratio: float = 0.2,
    progress_cb=None,
) -> Dict[str, Any]:
    results = []
    total = max(1, len(model_types) * len(target_keys))
    i = 0
    for mt in model_types:
        for tk in target_keys:
            i += 1
            mid = f"{mt[:3]}-{tk.replace('_', '')}-{i:02d}"
            # uniquify
            existing = {m["model_id"] for m in list_models(league_id)}
            base = mid
            n = 1
            while mid in existing:
                n += 1
                mid = f"{base}-{n}"
            if progress_cb:
                progress_cb(i / total * 0.95, f"Training {mid}...")
            try:
                results.append(
                    train_model_sync(
                        league_id=league_id,
                        model_id=mid,
                        model_type=mt,
                        target_key=tk,
                        eval_ratio=eval_ratio,
                    )
                )
            except Exception as exc:
                results.append({"league_id": league_id, "model_id": mid, "error": str(exc)})
    return {"league_id": league_id, "trained": results, "count": len(results)}


def load_trained_model(league_id: str, model_id: str):
    mdb = ModelDatabase(league_id=league_id)
    return mdb.load_model(model_id=model_id)
