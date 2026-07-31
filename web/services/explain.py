from __future__ import annotations

import base64
from io import BytesIO
from typing import Any, Dict, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.preprocessing.utils.target import class_names
from web.services.leagues import load_league_frame
from web.services.models import load_trained_model


def _explainer_map():
    try:
        from src.interpretability.explainers import (
            DecisionTreeExplainer,
            DiscriminantAnalysisExplainer,
            ExtremeBoostingExplainer,
            KNNExplainer,
            LogisticRegressionExplainer,
            NaiveBayesExplainer,
            NeuralNetworkExplainer,
            RandomForestExplainer,
            SVMExplainer,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Explainability dependencies missing. Rebuild with "
            "REQUIREMENTS_FILE=requirements-analysis.txt. "
            f"Detail: {exc}"
        ) from exc

    mapping = {
        "LogisticRegressor": LogisticRegressionExplainer,
        "logistic": LogisticRegressionExplainer,
        "DiscriminantAnalysisClassifier": DiscriminantAnalysisExplainer,
        "discriminant": DiscriminantAnalysisExplainer,
        "DecisionTree": DecisionTreeExplainer,
        "decision_tree": DecisionTreeExplainer,
        "RandomForest": RandomForestExplainer,
        "random_forest": RandomForestExplainer,
        "XGBoost": ExtremeBoostingExplainer,
        "xgboost": ExtremeBoostingExplainer,
        "KNN": KNNExplainer,
        "knn": KNNExplainer,
        "NaiveBayes": NaiveBayesExplainer,
        "naive_bayes": NaiveBayesExplainer,
        "SVM": SVMExplainer,
        "svm": SVMExplainer,
    }
    if NeuralNetworkExplainer is not None:
        mapping["NeuralNetwork"] = NeuralNetworkExplainer
        mapping["neural_network"] = NeuralNetworkExplainer
    return mapping


def _fig_to_base64() -> str:
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    plt.close("all")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def explain_model(
    *,
    league_id: str,
    model_id: str,
    plot_type: str = "shap_bar",
    target_label: Optional[str] = None,
    feature_a: str = "1",
    feature_b: str = "X",
    match_index: int = 0,
    model_type_hint: str = "",
) -> Dict[str, Any]:
    df = load_league_frame(league_id)
    if df is None:
        raise ValueError("League not found")
    df = df.dropna().reset_index(drop=True)

    model, config = load_trained_model(league_id, model_id)
    if model is None:
        raise ValueError("Model not found")

    cls_name = type(model).__name__
    explainer_map = _explainer_map()
    explainer_cls = explainer_map.get(model_type_hint) or explainer_map.get(cls_name)
    if explainer_cls is None:
        raise ValueError(f"No explainer for model class {cls_name}")

    # Use train slice for SHAP background
    num_eval = int((config or {}).get("num_eval_samples") or max(1, int(df.shape[0] * 0.2)))
    train_df = df.iloc[num_eval:].reset_index(drop=True)
    if train_df.shape[0] < 20:
        train_df = df

    plt.close("all")
    explainer = explainer_cls(model=model, df=train_df)
    labels = class_names(model.target_type)
    target_label = target_label or labels[0]

    needs_shap = plot_type in ("shap_bar", "waterfall")
    if needs_shap:
        try:
            explainer.compute_shap_values()
        except Exception as exc:
            if plot_type != "boundary":
                raise RuntimeError(f"SHAP unavailable for this model: {exc}") from exc

    if plot_type == "shap_bar":
        ax = explainer.shap_bar_plot(target=target_label, clustering=False)
        if ax is None:
            raise RuntimeError("SHAP bar plot not available for this model.")
    elif plot_type == "waterfall":
        explainer.instance_waterfall_plot(match_index=int(match_index), target=target_label)
    elif plot_type == "pdp":
        explainer.partial_dependence_plot(feature=feature_a, target=target_label)
    elif plot_type == "boundary":
        explainer.boundary_plot(features=[feature_a, feature_b])
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    return {
        "league_id": league_id,
        "model_id": model_id,
        "plot_type": plot_type,
        "target_label": target_label,
        "class_names": labels,
        "image_b64": _fig_to_base64(),
        "features": train_df.columns.tolist(),
    }
