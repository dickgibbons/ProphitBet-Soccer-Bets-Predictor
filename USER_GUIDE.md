# ProphitBet Web — User Guide

Soccer ML tool for downloading league history, training many models/targets, evaluating filters, research sweeps, fixtures, and analysis.

**Open it:** [https://gibbonsai.com/prophitbet/](https://gibbonsai.com/prophitbet/)

**Disclaimer:** Research / decision-support software. Past accuracy does not guarantee future results. Bet responsibly.

---

## Quick start

1. **New League** — pick a competition, keep the auto ID, start year ≥ 2015, create; wait for the job.
2. **Models** — batch-train RF/XGB/LR on Result + O/U, or open **Train** for full knobs.
3. **Evaluate** — Dataset = **Eval**; try odd ranges and mild probability filters; export CSV.
4. **Research** — select leagues → start sweep job → open the report for ranked Eval edges.
5. **Predict** / **Fixtures** — manual match or weekend slate (CSV always works; scrape needs fixtures image).

---

## Concepts

| Term | Meaning |
|------|---------|
| **League** | Saved dataset (CSV + form features). |
| **Model** | Trained classifier for one league + one target. |
| **Train / Eval** | Older fit set vs most-recent holdout. |
| **Profit Balance** | Result-only metric; if **lower than accuracy**, ProphitBet treats the filter as mathematically profitable. |
| **Research sweep** | Automated train + filter grid ranked by unit-stake ROI on Eval. |

---

## 1. Leagues

**Fields:** competition, unique ID, start year, history window (2–5), goal-diff margin (2–5).

**Update league data** on the league page re-downloads and rebuilds stats.

Prefer **2015+** and history window **3**. Changing history/margin needs a new league.

---

## 2. Train / Models

### Algorithms
Logistic, Discriminant (LDA/QDA), Decision Tree, Random Forest, XGBoost, KNN, Naive Bayes, SVM.  
**Deep Neural Network** only on the `full-ml` Docker image.

### Targets
| Target | Classes |
|--------|---------|
| Result (1/X/2) | H / D / A |
| Over/Under 2.5 | U / O |
| Over/Under 1.5 | U1.5 / O1.5 |
| Over/Under 3.5 | U3.5 / O3.5 |
| BTTS | No / Yes |

Profit Balance / priced ROI apply to **Result** (1X2 odds). Binary targets report classification metrics only unless you add market odds yourself.

### Knobs
- **Normalizer:** None / Standard / Min-Max / Max-Abs  
- **Sampler:** None / SVM-SMOTE / Near-Miss / Instance Hardness  
- **Calibration:** on/off (not for Discriminant / DNN)  
- **Eval ratio:** 5%–40% (most recent holdout)  
- **K-fold / sliding CV** optional  
- **Optuna:** optional trials maximizing Accuracy/F1/Precision/Recall  

**Model manager** lists models, batch-trains grids of algorithm × target, links to Evaluate / Explain.

---

## 3. Evaluate

Dataset **Eval** for honest scores. Odd ranges + probability percentiles filter niches. Seasonal table breaks accuracy by season. Export filtered preview as CSV/Excel.

---

## 4. Research

Runs the same sweep used in CLI (`scripts/research_sweep.py`): ensures models exist, grids filters, writes `data/research/sweep-*.json`, shows global top edges. Prefer edges with large **n** that repeat across models.

---

## 5. Predict & Fixtures

**Manual:** home/away + 1/X/2 odds → predicted class + probabilities → session export.

**Fixtures:** date scrape via FootyStats (**fixtures** / **full-ml** image) **or** CSV upload (`Home,Away,1,X,2`). Fuzzy-matches team names to league history.

---

## 6. Analysis & Explain

Need **analysis** or **full-ml** image (`shap`, `Boruta`, …).

- **Analysis:** descriptions, distributions, variances, correlations, Boruta, coefficients, impurity, rules.  
- **Explain:** SHAP bar / waterfall / PDP / decision boundary for a trained model.

---

## Docker profiles (see DEPLOY.md)

| Profile | Use when |
|---------|----------|
| slim (default) | Daily train / eval / research |
| analysis | Charts + SHAP |
| fixtures | Weekend FootyStats scrape |
| full-ml | DNN + everything |

---

## Red flags

- Train ≫ Eval → overfit  
- Filter with &lt; ~30 matches → anecdote  
- Using **Train** metrics to pick bets → optimistic bias  
- Huge research ROI after thousands of filters → expect regression; paper-trade first  

---

## Cheat sheet

| Goal | Do this |
|------|---------|
| Fresh dataset | New League → job |
| Many models | Models → batch train |
| Full knobs / Optuna | Train form |
| Honest niche | Evaluate → Eval + filters |
| Scale search | Research page |
| Weekend slate | Fixtures (CSV or scrape) |
| Feature insight | Analysis / Explain |
