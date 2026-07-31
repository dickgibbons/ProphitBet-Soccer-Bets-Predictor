from __future__ import annotations

import base64
from io import BytesIO
from typing import Any, Dict, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.preprocessing.utils.target import TargetType
from web.services.leagues import load_league_frame
from web.services.models import TARGET_TYPES

ANALYSIS_TYPES = [
    {"value": "description", "label": "Descriptions"},
    {"value": "distributions", "label": "Distributions"},
    {"value": "variances", "label": "Variances"},
    {"value": "correlations", "label": "Correlations"},
    {"value": "boruta", "label": "Boruta Selections"},
    {"value": "coefficients", "label": "Coefficients"},
    {"value": "impurity", "label": "Impurity"},
    {"value": "rules", "label": "Rule Extraction"},
]


def _fig_to_base64() -> str:
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=120)
    plt.close("all")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def run_analysis(
    *,
    league_id: str,
    analysis_type: str,
    season: Optional[int] = None,
    target_key: str = "result",
    colormap: str = "Blues",
) -> Dict[str, Any]:
    df = load_league_frame(league_id)
    if df is None or df.empty:
        raise ValueError("League not found")
    df = df.dropna().reset_index(drop=True)
    target = TARGET_TYPES.get(target_key, TargetType.RESULT)
    plt.close("all")

    try:
        if analysis_type == "description":
            from src.analysis.description import DescriptiveAnalyzer

            analyzer = DescriptiveAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap)
        elif analysis_type == "distributions":
            from src.analysis.distributions import DistributionAnalyzer

            analyzer = DistributionAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap)
        elif analysis_type == "variances":
            from src.analysis.variance import VarianceAnalyzer

            analyzer = VarianceAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap)
        elif analysis_type == "correlations":
            from src.analysis.correlation import CorrelationAnalyzer

            analyzer = CorrelationAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap)
        elif analysis_type == "boruta":
            from src.analysis.boruta_ import BorutaAnalyzer

            analyzer = BorutaAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap, target_type=target)
        elif analysis_type == "coefficients":
            from src.analysis.coefficients import CoefficientsAnalyzer

            analyzer = CoefficientsAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap, target_type=target)
        elif analysis_type == "impurity":
            from src.analysis.impurity import ImpurityAnalyzer

            analyzer = ImpurityAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap, target_type=target)
        elif analysis_type == "rules":
            from src.analysis.rules import RulesAnalyzer

            analyzer = RulesAnalyzer(df=df)
            analyzer.generate_plot(season=season, colormap=colormap, target_type=target)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
    except ImportError as exc:
        raise RuntimeError(
            "Analysis dependencies missing. Rebuild with REQUIREMENTS_FILE=requirements-analysis.txt "
            f"(or requirements-full-ml.txt). Detail: {exc}"
        ) from exc

    return {
        "league_id": league_id,
        "analysis_type": analysis_type,
        "image_b64": _fig_to_base64(),
    }
