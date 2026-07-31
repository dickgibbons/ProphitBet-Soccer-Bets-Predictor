# ProphitBet Playbook — Healthy Edges (ROI > 20%)

_Generated 2026-07-31 UTC from: sweep-live.json (2026-07-31T03:35:50Z), sweep-all-new.json (2026-07-31T16:14:04Z)_

## How to read this

Each edge is an **Eval-set** filter mined by the research sweep:

1. Open the league → **Evaluate** the listed model
2. Dataset: **Eval**
3. Set the **odds range** and **probability percentiles** exactly as listed
4. Flat 1-unit stake on the model’s predicted outcome within that filter

**ROI** = mean profit per unit stake on filtered Eval bets. **n** = filtered sample count.

### Health tiers

| Tier | Rule | Meaning |
|------|------|---------|
| **A** | n ≥ 80, ROI > 20% | Best sample support — prioritize |
| **B** | n ≥ 60, ROI > 20% | Solid |
| **C** | n ≥ 50, ROI > 20% | Usable, watch variance |
| **D** | n 40–49, ROI > 20% | Thin — paper-trade first |

Near-duplicate percentile variants for the same league/model/odds band are collapsed to the **best ROI** setting.

**Coverage:** 94 distinct edges across 26 leagues (309 raw filters with ROI>20% before dedupe).

### Caveats

- Edges are **in-sample on Eval** (last ~20% of matches). Expect live ROI to shrink.
- Small-n / high-percentile filters overfit easily — prefer Tier A/B.
- MLS excluded (training failed on odds cells with `'x'`).
- Bundesliga 1 historically near-flat in earlier sweeps; only include if it appears below.

## Master table (all healthy edges)

| Tier | ROI | n | Units | Acc | League | Model | Odds filter | Prob filter |
|------|-----|---|-------|-----|--------|-------|-------------|-------------|
| D | +73.0% | 49 | 35.76 | 55.1% | Argentina Primera | rf-result | `2-[1.91,2.5]` | `p1=20,px=10,p2=10` |
| D | +59.1% | 42 | 24.82 | 64.3% | China Super League | lr-result | `2-[1.91,2.5]` | `p1=30` |
| D | +56.9% | 40 | 22.75 | 52.5% | Argentina Primera | rf-result | `1-[3.51,100]` | `p1=10,px=10,p2=10` |
| D | +55.2% | 41 | 22.63 | 61.0% | Sweden Allsvenskan | xgb-result | `2-[1.91,2.5]` | `px=20` |
| C | +47.0% | 54 | 25.36 | 64.8% | Italy Serie A | lr-result | `2-[1.91,2.5]` | `p1=10,px=10,p2=10` |
| D | +46.8% | 41 | 19.17 | 58.5% | China Super League | rf-result | `2-[1.91,2.5]` | `px=10` |
| D | +44.0% | 44 | 19.35 | 59.1% | China Super League | lr-result | `1-[2.5,3.5]` | `p2=10` |
| C | +42.9% | 57 | 24.47 | 56.1% | Brazil Serie A | xgb-result | `2-[2.5,3.5]` | `p2=40` |
| D | +40.9% | 43 | 17.59 | 55.8% | Spain La Liga | xgb-result | `2-[1.91,2.5]` | `p2=40` |
| D | +40.8% | 46 | 18.77 | 56.5% | Sweden Allsvenskan | xgb-result | `1-[2.5,3.5]` | `p1=20,px=10,p2=10` |
| B | +40.6% | 62 | 25.19 | 53.2% | Spain La Liga | xgb-result | `1-[2.5,3.5]` | `p2=30` |
| B | +39.9% | 63 | 25.13 | 58.7% | Russia Premier League | lr-result | `2-[2.5,3.5]` | `p2=10` |
| D | +39.0% | 40 | 15.59 | 77.5% | Germany Bundesliga 2 | svm-result | `1-[1.61,1.9]` | `px=40` |
| C | +37.7% | 55 | 20.74 | 49.1% | Greece Super League | rf-result | `2-[2.5,3.5]` | `p2=40` |
| D | +37.5% | 43 | 16.12 | 51.2% | Italy Serie A | lr-result | `1-[2.5,3.5]` | `px=40` |
| D | +37.3% | 40 | 14.91 | 47.5% | Greece Super League | rf-result | `1-[1.91,2.5]` | `p2=40` |
| D | +35.2% | 40 | 14.09 | 52.5% | Greece Super League | svm-result | `1-[2.5,3.5]` | `p2=30` |
| A | +35.0% | 94 | 32.87 | 54.3% | England Premier League | xgb-result | `2-[2.5,3.5]` | `p2=40` |
| D | +34.9% | 40 | 13.96 | 50.0% | Spain Segunda | xgb-result | `2-[1.91,2.5]` | `p2=30` |
| D | +34.8% | 41 | 14.28 | 68.3% | Scotland Premiership | svm-result | `1-[1.61,1.9]` | `p2=10` |
| B | +34.8% | 63 | 21.92 | 49.2% | Scotland Premiership | xgb-result | `1-[2.5,3.5]` | `p2=30` |
| C | +34.7% | 53 | 18.37 | 54.7% | Spain La Liga | svm-result | `2-[1.91,2.5]` | `p2=40` |
| D | +34.6% | 42 | 14.54 | 59.5% | Italy Serie A | rf-result | `2-[1.91,2.5]` | `px=40` |
| D | +34.4% | 42 | 14.46 | 52.4% | Greece Super League | rf-result | `1-[2.5,3.5]` | `p2=30` |
| D | +34.4% | 41 | 14.09 | 51.2% | France Ligue 2 | svm-result | `X-[2.0,3.0]` | `none` |
| D | +34.2% | 46 | 15.75 | 60.9% | Russia Premier League | rf-result | `1-[1.91,2.5]` | `p1=10,px=10,p2=10` |
| D | +34.0% | 43 | 14.6 | 55.8% | Scotland Premiership | lr-result | `2-[2.5,3.5]` | `p2=30` |
| C | +33.8% | 55 | 18.61 | 52.7% | Spain La Liga | svm-result | `1-[2.5,3.5]` | `p2=40` |
| C | +33.6% | 54 | 18.12 | 51.9% | Romania Liga 1 | xgb-result | `X-[2.0,3.0]` | `px=30` |
| C | +33.6% | 53 | 17.78 | 50.9% | Russia Premier League | lr-result | `1-[2.5,3.5]` | `p1=40` |
| D | +33.5% | 44 | 14.73 | 50.0% | Russia Premier League | xgb-result | `1-[2.5,3.5]` | `px=20` |
| C | +33.3% | 54 | 17.99 | 51.9% | France Ligue 1 | svm-result | `2-[2.5,3.5]` | `px=20` |
| D | +32.7% | 42 | 13.74 | 57.1% | Spain La Liga | rf-result | `2-[1.91,2.5]` | `p1=10` |
| D | +32.6% | 43 | 14.0 | 46.5% | Scotland Premiership | xgb-result | `2-[1.91,2.5]` | `p2=30` |
| C | +31.4% | 58 | 18.23 | 56.9% | Turkey Super Lig | svm-result | `1-[1.91,2.5]` | `p2=20` |
| B | +31.3% | 61 | 19.12 | 54.1% | Spain Segunda | svm-result | `2-[1.91,2.5]` | `p2=30` |
| D | +31.3% | 42 | 13.14 | 57.1% | Brazil Serie A | svm-result | `1-[1.91,2.5]` | `p2=40` |
| B | +31.1% | 66 | 20.5 | 72.7% | Germany Bundesliga 2 | svm-result | `2-[3.51,100]` | `px=40` |
| D | +31.0% | 46 | 14.28 | 52.2% | Turkey Super Lig | lr-result | `2-[2.5,3.5]` | `p2=30` |
| D | +31.0% | 45 | 13.96 | 57.8% | Japan J1 | svm-result | `2-[1.91,2.5]` | `px=20` |
| D | +31.0% | 41 | 12.7 | 48.8% | Scotland Premiership | rf-result | `1-[2.5,3.5]` | `p1=20,px=10,p2=10` |
| B | +30.7% | 61 | 18.72 | 52.5% | Turkey Super Lig | rf-result | `1-[2.5,3.5]` | `p1=40` |
| C | +29.3% | 58 | 17.01 | 72.4% | Germany Bundesliga 2 | dt-result | `1-[1.61,1.9]` | `px=10` |
| C | +29.1% | 52 | 15.16 | 65.4% | Russia Premier League | rf-result | `2-[3.51,100]` | `px=40` |
| B | +28.7% | 65 | 18.67 | 49.2% | Spain La Liga | rf-result | `1-[2.5,3.5]` | `px=40` |
| C | +28.3% | 59 | 16.68 | 47.5% | Brazil Serie A | lr-result | `1-[2.5,3.5]` | `p1=20,px=10,p2=10` |
| B | +28.2% | 66 | 18.61 | 53.0% | Spain Segunda | lr-result | `2-[1.91,2.5]` | `p2=30` |
| B | +28.2% | 64 | 18.03 | 53.1% | Turkey Super Lig | svm-result | `2-[2.5,3.5]` | `p2=20` |
| A | +28.1% | 83 | 23.29 | 54.2% | Mexico Liga MX | xgb-result | `2-[2.5,3.5]` | `p1=10,px=10,p2=10` |
| D | +27.3% | 42 | 11.48 | 50.0% | Greece Super League | lr-result | `1-[2.5,3.5]` | `p2=30` |
| D | +27.2% | 43 | 11.7 | 53.5% | Denmark Superliga | lr-result | `2-[2.5,3.5]` | `p2=40` |
| D | +27.0% | 42 | 11.32 | 50.0% | England Premier League | xgb-result | `1-[2.5,3.5]` | `px=20` |
| B | +26.9% | 67 | 18.05 | 50.7% | France Ligue 2 | svm-result | `2-[2.5,3.5]` | `px=40` |
| B | +26.9% | 73 | 19.66 | 54.8% | Mexico Liga MX | xgb-result | `1-[1.91,2.5]` | `p2=30` |
| D | +26.8% | 49 | 13.12 | 53.1% | Norway Eliteserien | rf-result | `2-[2.5,3.5]` | `p1=10,px=10,p2=10` |
| D | +26.6% | 45 | 11.98 | 57.8% | Portugal Liga 1 | dt-result | `1-[1.91,2.5]` | `px=20` |
| B | +26.6% | 60 | 15.95 | 51.7% | Scotland Premiership | xgb-result | `2-[2.5,3.5]` | `p2=30` |
| A | +26.6% | 88 | 23.38 | 52.3% | England Premier League | xgb-result | `1-[1.91,2.5]` | `p2=40` |
| B | +26.3% | 70 | 18.42 | 50.0% | Spain Segunda | svm-result | `1-[2.5,3.5]` | `p2=30` |
| C | +26.1% | 50 | 13.04 | 66.0% | Japan J1 | lr-result | `2-[3.51,100]` | `p2=40` |
| D | +26.0% | 40 | 10.4 | 67.5% | Switzerland Super League | xgb-result | `1-[1.61,1.9]` | `px=30` |
| B | +25.8% | 69 | 17.8 | 69.6% | Germany Bundesliga 2 | lr-result | `2-[3.51,100]` | `px=40` |
| C | +25.3% | 50 | 12.67 | 60.0% | Italy Serie A | lr-result | `2-[3.51,100]` | `p2=30` |
| D | +25.0% | 44 | 11.0 | 59.1% | Mexico Liga MX | dt-result | `1-[1.91,2.5]` | `px=20` |
| C | +24.6% | 57 | 14.03 | 70.2% | Germany Bundesliga 2 | rf-result | `1-[1.61,1.9]` | `px=30` |
| B | +24.6% | 63 | 15.48 | 52.4% | Belgium Jupiler | rf-result | `1-[2.5,3.5]` | `p1=30` |
| B | +24.5% | 61 | 14.95 | 47.5% | Portugal Liga 1 | xgb-result | `2-[2.5,3.5]` | `p2=40` |
| D | +24.5% | 45 | 11.03 | 55.6% | Switzerland Super League | xgb-result | `2-[2.5,3.5]` | `px=30` |
| D | +24.3% | 40 | 9.72 | 55.0% | Italy Serie A | svm-result | `2-[1.91,2.5]` | `p1=20,px=10,p2=10` |
| B | +24.3% | 62 | 15.05 | 58.1% | Turkey Super Lig | dt-result | `1-[1.91,2.5]` | `px=20` |
| B | +24.2% | 75 | 18.18 | 49.3% | Brazil Serie A | lr-result | `2-[2.5,3.5]` | `p2=30` |
| D | +24.0% | 46 | 11.04 | 47.8% | France Ligue 2 | lr-result | `2-[1.91,2.5]` | `px=30` |
| B | +23.8% | 78 | 18.54 | 51.3% | France Ligue 2 | svm-result | `1-[1.91,2.5]` | `px=40` |
| B | +23.7% | 64 | 15.19 | 65.6% | Japan J1 | svm-result | `2-[3.51,100]` | `p2=40` |
| D | +23.7% | 49 | 11.63 | 51.0% | Norway Eliteserien | xgb-result | `2-[2.5,3.5]` | `p2=40` |
| D | +23.6% | 45 | 10.63 | 48.9% | Belgium Jupiler | svm-result | `2-[2.5,3.5]` | `px=30` |
| B | +23.4% | 64 | 14.96 | 34.4% | France Ligue 1 | dt-result | `1-[3.51,100]` | `px=10` |
| D | +23.4% | 46 | 10.75 | 84.8% | Spain La Liga | dt-result | `1-[1.31,1.6]` | `px=30` |
| D | +23.4% | 49 | 11.44 | 69.4% | England Championship | rf-result | `1-[1.61,1.9]` | `p2=30` |
| A | +23.1% | 92 | 21.28 | 50.0% | England Premier League | rf-result | `2-[2.5,3.5]` | `p2=40` |
| C | +23.1% | 58 | 13.38 | 69.0% | Germany Bundesliga 2 | lr-result | `1-[1.61,1.9]` | `px=30` |
| C | +23.0% | 52 | 11.95 | 48.1% | Romania Liga 1 | rf-result | `X-[2.0,3.0]` | `p2=40` |
| D | +22.9% | 49 | 11.21 | 49.0% | Portugal Liga 1 | xgb-result | `1-[1.91,2.5]` | `p2=40` |
| D | +22.6% | 46 | 10.41 | 54.3% | England League Two | xgb-result | `1-[1.91,2.5]` | `px=40` |
| B | +22.6% | 72 | 16.24 | 55.6% | Mexico Liga MX | rf-result | `1-[1.91,2.5]` | `px=20` |
| A | +22.4% | 89 | 19.96 | 47.2% | Spain Segunda | lr-result | `1-[2.5,3.5]` | `p2=20` |
| D | +21.7% | 49 | 10.65 | 51.0% | Norway Eliteserien | xgb-result | `1-[1.91,2.5]` | `p2=40` |
| D | +21.4% | 49 | 10.47 | 44.9% | Romania Liga 1 | xgb-result | `2-[2.5,3.5]` | `px=40` |
| D | +21.2% | 40 | 8.47 | 47.5% | France Ligue 2 | rf-result | `X-[2.0,3.0]` | `p1=10` |
| D | +21.0% | 45 | 9.44 | 73.3% | Denmark Superliga | rf-result | `2-[3.51,100]` | `p2=20` |
| A | +20.8% | 90 | 18.72 | 68.9% | Germany Bundesliga 2 | xgb-result | `2-[3.51,100]` | `p1=10,px=10,p2=10` |
| C | +20.8% | 51 | 10.6 | 47.1% | England Championship | xgb-result | `1-[3.51,100]` | `p1=30` |
| D | +20.6% | 43 | 8.87 | 48.8% | Ireland Premier | svm-result | `1-[1.91,2.5]` | `px=10` |
| D | +20.3% | 41 | 8.33 | 82.9% | Spain La Liga | xgb-result | `1-[1.31,1.6]` | `p2=10` |

## Priority card — Tier A & B

### Spain La Liga — xgb-result (B)

- **ROI:** +40.6% on **n=62** (profit units ≈ 25.19)
- **Accuracy:** 53.2% · F1 0.483
- **Model:** XGBoost · Result (`La-Liga-Spain-02` / `xgb-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Russia Premier League — lr-result (B)

- **ROI:** +39.9% on **n=63** (profit units ≈ 25.13)
- **Accuracy:** 58.7% · F1 0.424
- **Model:** Logistic Regression · Result (`Premier-League-Russia-01` / `lr-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 10th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 10}`

### England Premier League — xgb-result (A)

- **ROI:** +35.0% on **n=94** (profit units ≈ 32.87)
- **Accuracy:** 54.3% · F1 0.380
- **Model:** XGBoost · Result (`Premier-League-England-01` / `xgb-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 40}`

### Scotland Premiership — xgb-result (B)

- **ROI:** +34.8% on **n=63** (profit units ≈ 21.92)
- **Accuracy:** 49.2% · F1 0.448
- **Model:** XGBoost · Result (`Premiership-Scotland-01` / `xgb-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Spain Segunda — svm-result (B)

- **ROI:** +31.3% on **n=61** (profit units ≈ 19.12)
- **Accuracy:** 54.1% · F1 0.462
- **Model:** SVM · Result (`Segunda-Division-Spain-01` / `svm-result`)
- **Odds filter:** Away odds in [1.91,2.5] (`odd_key=13` → `2-[1.91,2.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Germany Bundesliga 2 — svm-result (B)

- **ROI:** +31.1% on **n=66** (profit units ≈ 20.5)
- **Accuracy:** 72.7% · F1 0.283
- **Model:** SVM · Result (`Bundesliga-2-Germany-01` / `svm-result`)
- **Odds filter:** Away odds in [3.51,100] (`odd_key=15` → `2-[3.51,100]`)
- **Prob filter:** Draw prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 40, "p2": 0}`

### Turkey Super Lig — rf-result (B)

- **ROI:** +30.7% on **n=61** (profit units ≈ 18.72)
- **Accuracy:** 52.5% · F1 0.430
- **Model:** Random Forest · Result (`Super-Lig-Turkey-01` / `rf-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Home prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 40, "px": 0, "p2": 0}`

### Spain La Liga — rf-result (B)

- **ROI:** +28.7% on **n=65** (profit units ≈ 18.67)
- **Accuracy:** 49.2% · F1 0.477
- **Model:** Random Forest · Result (`La-Liga-Spain-02` / `rf-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Draw prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 40, "p2": 0}`

### Spain Segunda — lr-result (B)

- **ROI:** +28.2% on **n=66** (profit units ≈ 18.61)
- **Accuracy:** 53.0% · F1 0.456
- **Model:** Logistic Regression · Result (`Segunda-Division-Spain-01` / `lr-result`)
- **Odds filter:** Away odds in [1.91,2.5] (`odd_key=13` → `2-[1.91,2.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Turkey Super Lig — svm-result (B)

- **ROI:** +28.2% on **n=64** (profit units ≈ 18.03)
- **Accuracy:** 53.1% · F1 0.414
- **Model:** SVM · Result (`Super-Lig-Turkey-01` / `svm-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 20th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 20}`

### Mexico Liga MX — xgb-result (A)

- **ROI:** +28.1% on **n=83** (profit units ≈ 23.29)
- **Accuracy:** 54.2% · F1 0.367
- **Model:** XGBoost · Result (`Liga-MX-Mexico-01` / `xgb-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Home prob ≥ 10th percentile of the filtered Eval set; Draw prob ≥ 10th percentile of the filtered Eval set; Away prob ≥ 10th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 10, "px": 10, "p2": 10}`

### France Ligue 2 — svm-result (B)

- **ROI:** +26.9% on **n=67** (profit units ≈ 18.05)
- **Accuracy:** 50.7% · F1 0.442
- **Model:** SVM · Result (`Ligue-2-France-01` / `svm-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Draw prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 40, "p2": 0}`

### Mexico Liga MX — xgb-result (B)

- **ROI:** +26.9% on **n=73** (profit units ≈ 19.66)
- **Accuracy:** 54.8% · F1 0.389
- **Model:** XGBoost · Result (`Liga-MX-Mexico-01` / `xgb-result`)
- **Odds filter:** Home odds in [1.91,2.5] (`odd_key=4` → `1-[1.91,2.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Scotland Premiership — xgb-result (B)

- **ROI:** +26.6% on **n=60** (profit units ≈ 15.95)
- **Accuracy:** 51.7% · F1 0.390
- **Model:** XGBoost · Result (`Premiership-Scotland-01` / `xgb-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### England Premier League — xgb-result (A)

- **ROI:** +26.6% on **n=88** (profit units ≈ 23.38)
- **Accuracy:** 52.3% · F1 0.353
- **Model:** XGBoost · Result (`Premier-League-England-01` / `xgb-result`)
- **Odds filter:** Home odds in [1.91,2.5] (`odd_key=4` → `1-[1.91,2.5]`)
- **Prob filter:** Away prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 40}`

### Spain Segunda — svm-result (B)

- **ROI:** +26.3% on **n=70** (profit units ≈ 18.42)
- **Accuracy:** 50.0% · F1 0.428
- **Model:** SVM · Result (`Segunda-Division-Spain-01` / `svm-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### Germany Bundesliga 2 — lr-result (B)

- **ROI:** +25.8% on **n=69** (profit units ≈ 17.8)
- **Accuracy:** 69.6% · F1 0.276
- **Model:** Logistic Regression · Result (`Bundesliga-2-Germany-01` / `lr-result`)
- **Odds filter:** Away odds in [3.51,100] (`odd_key=15` → `2-[3.51,100]`)
- **Prob filter:** Draw prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 40, "p2": 0}`

### Belgium Jupiler — rf-result (B)

- **ROI:** +24.6% on **n=63** (profit units ≈ 15.48)
- **Accuracy:** 52.4% · F1 0.344
- **Model:** Random Forest · Result (`Jupiler-League-Belgium-01` / `rf-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Home prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 30, "px": 0, "p2": 0}`

### Portugal Liga 1 — xgb-result (B)

- **ROI:** +24.5% on **n=61** (profit units ≈ 14.95)
- **Accuracy:** 47.5% · F1 0.449
- **Model:** XGBoost · Result (`Liga-1-Portugal-01` / `xgb-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 40}`

### Turkey Super Lig — dt-result (B)

- **ROI:** +24.3% on **n=62** (profit units ≈ 15.05)
- **Accuracy:** 58.1% · F1 0.245
- **Model:** Decision Tree · Result (`Super-Lig-Turkey-01` / `dt-result`)
- **Odds filter:** Home odds in [1.91,2.5] (`odd_key=4` → `1-[1.91,2.5]`)
- **Prob filter:** Draw prob ≥ 20th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 20, "p2": 0}`

### Brazil Serie A — lr-result (B)

- **ROI:** +24.2% on **n=75** (profit units ≈ 18.18)
- **Accuracy:** 49.3% · F1 0.396
- **Model:** Logistic Regression · Result (`Serie-A-Brazil-01` / `lr-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 30th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 30}`

### France Ligue 2 — svm-result (B)

- **ROI:** +23.8% on **n=78** (profit units ≈ 18.54)
- **Accuracy:** 51.3% · F1 0.423
- **Model:** SVM · Result (`Ligue-2-France-01` / `svm-result`)
- **Odds filter:** Home odds in [1.91,2.5] (`odd_key=4` → `1-[1.91,2.5]`)
- **Prob filter:** Draw prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 40, "p2": 0}`

### Japan J1 — svm-result (B)

- **ROI:** +23.7% on **n=64** (profit units ≈ 15.19)
- **Accuracy:** 65.6% · F1 0.264
- **Model:** SVM · Result (`J-1-Japan-01` / `svm-result`)
- **Odds filter:** Away odds in [3.51,100] (`odd_key=15` → `2-[3.51,100]`)
- **Prob filter:** Away prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 40}`

### France Ligue 1 — dt-result (B)

- **ROI:** +23.4% on **n=64** (profit units ≈ 14.96)
- **Accuracy:** 34.4% · F1 0.237
- **Model:** Decision Tree · Result (`Ligue-1-France-02` / `dt-result`)
- **Odds filter:** Home odds in [3.51,100] (`odd_key=6` → `1-[3.51,100]`)
- **Prob filter:** Draw prob ≥ 10th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 10, "p2": 0}`

### England Premier League — rf-result (A)

- **ROI:** +23.1% on **n=92** (profit units ≈ 21.28)
- **Accuracy:** 50.0% · F1 0.357
- **Model:** Random Forest · Result (`Premier-League-England-01` / `rf-result`)
- **Odds filter:** Away odds in [2.5,3.5] (`odd_key=14` → `2-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 40th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 40}`

### Mexico Liga MX — rf-result (B)

- **ROI:** +22.6% on **n=72** (profit units ≈ 16.24)
- **Accuracy:** 55.6% · F1 0.382
- **Model:** Random Forest · Result (`Liga-MX-Mexico-01` / `rf-result`)
- **Odds filter:** Home odds in [1.91,2.5] (`odd_key=4` → `1-[1.91,2.5]`)
- **Prob filter:** Draw prob ≥ 20th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 20, "p2": 0}`

### Spain Segunda — lr-result (A)

- **ROI:** +22.4% on **n=89** (profit units ≈ 19.96)
- **Accuracy:** 47.2% · F1 0.435
- **Model:** Logistic Regression · Result (`Segunda-Division-Spain-01` / `lr-result`)
- **Odds filter:** Home odds in [2.5,3.5] (`odd_key=5` → `1-[2.5,3.5]`)
- **Prob filter:** Away prob ≥ 20th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 0, "px": 0, "p2": 20}`

### Germany Bundesliga 2 — xgb-result (A)

- **ROI:** +20.8% on **n=90** (profit units ≈ 18.72)
- **Accuracy:** 68.9% · F1 0.274
- **Model:** XGBoost · Result (`Bundesliga-2-Germany-01` / `xgb-result`)
- **Odds filter:** Away odds in [3.51,100] (`odd_key=15` → `2-[3.51,100]`)
- **Prob filter:** Home prob ≥ 10th percentile of the filtered Eval set; Draw prob ≥ 10th percentile of the filtered Eval set; Away prob ≥ 10th percentile of the filtered Eval set
- **Evaluate presets:** percentiles `{"p1": 10, "px": 10, "p2": 10}`

## By league

### Argentina Primera

_League id:_ `Primera-Division-Argentina-01` · **2** healthy edges · best ROI **+73.0%**

- **[D]** `rf-result` · `2-[1.91,2.5]` · p=`{"p1":20,"px":10,"p2":10}` · **ROI +73.0%** · n=49 · acc=55.1% · units=35.76
- **[D]** `rf-result` · `1-[3.51,100]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +56.9%** · n=40 · acc=52.5% · units=22.75

### China Super League

_League id:_ `Super-League-China-01` · **3** healthy edges · best ROI **+59.1%**

- **[D]** `lr-result` · `2-[1.91,2.5]` · p=`{"p1":30,"px":0,"p2":0}` · **ROI +59.1%** · n=42 · acc=64.3% · units=24.82
- **[D]** `rf-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":10,"p2":0}` · **ROI +46.8%** · n=41 · acc=58.5% · units=19.17
- **[D]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":10}` · **ROI +44.0%** · n=44 · acc=59.1% · units=19.35

### Sweden Allsvenskan

_League id:_ `Allsvenskan-Sweden-01` · **2** healthy edges · best ROI **+55.2%**

- **[D]** `xgb-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +55.2%** · n=41 · acc=61.0% · units=22.63
- **[D]** `xgb-result` · `1-[2.5,3.5]` · p=`{"p1":20,"px":10,"p2":10}` · **ROI +40.8%** · n=46 · acc=56.5% · units=18.77

### Italy Serie A

_League id:_ `Serie-A-Italy-02` · **5** healthy edges · best ROI **+47.0%**

- **[C]** `lr-result` · `2-[1.91,2.5]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +47.0%** · n=54 · acc=64.8% · units=25.36
- **[D]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +37.5%** · n=43 · acc=51.2% · units=16.12
- **[D]** `rf-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +34.6%** · n=42 · acc=59.5% · units=14.54
- **[C]** `lr-result` · `2-[3.51,100]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +25.3%** · n=50 · acc=60.0% · units=12.67
- **[D]** `svm-result` · `2-[1.91,2.5]` · p=`{"p1":20,"px":10,"p2":10}` · **ROI +24.3%** · n=40 · acc=55.0% · units=9.72

### Brazil Serie A

_League id:_ `Serie-A-Brazil-01` · **4** healthy edges · best ROI **+42.9%**

- **[C]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +42.9%** · n=57 · acc=56.1% · units=24.47
- **[D]** `svm-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +31.3%** · n=42 · acc=57.1% · units=13.14
- **[C]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":20,"px":10,"p2":10}` · **ROI +28.3%** · n=59 · acc=47.5% · units=16.68
- **[B]** `lr-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +24.2%** · n=75 · acc=49.3% · units=18.18

### Spain La Liga

_League id:_ `La-Liga-Spain-02` · **8** healthy edges · best ROI **+40.9%**

- **[D]** `xgb-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +40.9%** · n=43 · acc=55.8% · units=17.59
- **[B]** `xgb-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +40.6%** · n=62 · acc=53.2% · units=25.19
- **[C]** `svm-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +34.7%** · n=53 · acc=54.7% · units=18.37
- **[C]** `svm-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +33.8%** · n=55 · acc=52.7% · units=18.61
- **[D]** `rf-result` · `2-[1.91,2.5]` · p=`{"p1":10,"px":0,"p2":0}` · **ROI +32.7%** · n=42 · acc=57.1% · units=13.74
- **[B]** `rf-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +28.7%** · n=65 · acc=49.2% · units=18.67
- **[D]** `dt-result` · `1-[1.31,1.6]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +23.4%** · n=46 · acc=84.8% · units=10.75
- **[D]** `xgb-result` · `1-[1.31,1.6]` · p=`{"p1":0,"px":0,"p2":10}` · **ROI +20.3%** · n=41 · acc=82.9% · units=8.33

### Russia Premier League

_League id:_ `Premier-League-Russia-01` · **5** healthy edges · best ROI **+39.9%**

- **[B]** `lr-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":10}` · **ROI +39.9%** · n=63 · acc=58.7% · units=25.13
- **[D]** `rf-result` · `1-[1.91,2.5]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +34.2%** · n=46 · acc=60.9% · units=15.75
- **[C]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":40,"px":0,"p2":0}` · **ROI +33.6%** · n=53 · acc=50.9% · units=17.78
- **[D]** `xgb-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +33.5%** · n=44 · acc=50.0% · units=14.73
- **[C]** `rf-result` · `2-[3.51,100]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +29.1%** · n=52 · acc=65.4% · units=15.16

### Germany Bundesliga 2

_League id:_ `Bundesliga-2-Germany-01` · **7** healthy edges · best ROI **+39.0%**

- **[D]** `svm-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +39.0%** · n=40 · acc=77.5% · units=15.59
- **[B]** `svm-result` · `2-[3.51,100]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +31.1%** · n=66 · acc=72.7% · units=20.5
- **[C]** `dt-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":10,"p2":0}` · **ROI +29.3%** · n=58 · acc=72.4% · units=17.01
- **[B]** `lr-result` · `2-[3.51,100]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +25.8%** · n=69 · acc=69.6% · units=17.8
- **[C]** `rf-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +24.6%** · n=57 · acc=70.2% · units=14.03
- **[C]** `lr-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +23.1%** · n=58 · acc=69.0% · units=13.38
- **[A]** `xgb-result` · `2-[3.51,100]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +20.8%** · n=90 · acc=68.9% · units=18.72

### Greece Super League

_League id:_ `Super-League-Greece-01` · **5** healthy edges · best ROI **+37.7%**

- **[C]** `rf-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +37.7%** · n=55 · acc=49.1% · units=20.74
- **[D]** `rf-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +37.3%** · n=40 · acc=47.5% · units=14.91
- **[D]** `svm-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +35.2%** · n=40 · acc=52.5% · units=14.09
- **[D]** `rf-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +34.4%** · n=42 · acc=52.4% · units=14.46
- **[D]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +27.3%** · n=42 · acc=50.0% · units=11.48

### England Premier League

_League id:_ `Premier-League-England-01` · **4** healthy edges · best ROI **+35.0%**

- **[A]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +35.0%** · n=94 · acc=54.3% · units=32.87
- **[D]** `xgb-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +27.0%** · n=42 · acc=50.0% · units=11.32
- **[A]** `xgb-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +26.6%** · n=88 · acc=52.3% · units=23.38
- **[A]** `rf-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +23.1%** · n=92 · acc=50.0% · units=21.28

### Spain Segunda

_League id:_ `Segunda-Division-Spain-01` · **5** healthy edges · best ROI **+34.9%**

- **[D]** `xgb-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +34.9%** · n=40 · acc=50.0% · units=13.96
- **[B]** `svm-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +31.3%** · n=61 · acc=54.1% · units=19.12
- **[B]** `lr-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +28.2%** · n=66 · acc=53.0% · units=18.61
- **[B]** `svm-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +26.3%** · n=70 · acc=50.0% · units=18.42
- **[A]** `lr-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":20}` · **ROI +22.4%** · n=89 · acc=47.2% · units=19.96

### Scotland Premiership

_League id:_ `Premiership-Scotland-01` · **6** healthy edges · best ROI **+34.8%**

- **[D]** `svm-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":0,"p2":10}` · **ROI +34.8%** · n=41 · acc=68.3% · units=14.28
- **[B]** `xgb-result` · `1-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +34.8%** · n=63 · acc=49.2% · units=21.92
- **[D]** `lr-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +34.0%** · n=43 · acc=55.8% · units=14.6
- **[D]** `xgb-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +32.6%** · n=43 · acc=46.5% · units=14.0
- **[D]** `rf-result` · `1-[2.5,3.5]` · p=`{"p1":20,"px":10,"p2":10}` · **ROI +31.0%** · n=41 · acc=48.8% · units=12.7
- **[B]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +26.6%** · n=60 · acc=51.7% · units=15.95

### France Ligue 2

_League id:_ `Ligue-2-France-01` · **5** healthy edges · best ROI **+34.4%**

- **[D]** `svm-result` · `X-[2.0,3.0]` · p=`{"p1":0,"px":0,"p2":0}` · **ROI +34.4%** · n=41 · acc=51.2% · units=14.09
- **[B]** `svm-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +26.9%** · n=67 · acc=50.7% · units=18.05
- **[D]** `lr-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +24.0%** · n=46 · acc=47.8% · units=11.04
- **[B]** `svm-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +23.8%** · n=78 · acc=51.3% · units=18.54
- **[D]** `rf-result` · `X-[2.0,3.0]` · p=`{"p1":10,"px":0,"p2":0}` · **ROI +21.2%** · n=40 · acc=47.5% · units=8.47

### Romania Liga 1

_League id:_ `Liga-1-Romania-01` · **3** healthy edges · best ROI **+33.6%**

- **[C]** `xgb-result` · `X-[2.0,3.0]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +33.6%** · n=54 · acc=51.9% · units=18.12
- **[C]** `rf-result` · `X-[2.0,3.0]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +23.0%** · n=52 · acc=48.1% · units=11.95
- **[D]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +21.4%** · n=49 · acc=44.9% · units=10.47

### France Ligue 1

_League id:_ `Ligue-1-France-02` · **2** healthy edges · best ROI **+33.3%**

- **[C]** `svm-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +33.3%** · n=54 · acc=51.9% · units=17.99
- **[B]** `dt-result` · `1-[3.51,100]` · p=`{"p1":0,"px":10,"p2":0}` · **ROI +23.4%** · n=64 · acc=34.4% · units=14.96

### Turkey Super Lig

_League id:_ `Super-Lig-Turkey-01` · **5** healthy edges · best ROI **+31.4%**

- **[C]** `svm-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":20}` · **ROI +31.4%** · n=58 · acc=56.9% · units=18.23
- **[D]** `lr-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +31.0%** · n=46 · acc=52.2% · units=14.28
- **[B]** `rf-result` · `1-[2.5,3.5]` · p=`{"p1":40,"px":0,"p2":0}` · **ROI +30.7%** · n=61 · acc=52.5% · units=18.72
- **[B]** `svm-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":20}` · **ROI +28.2%** · n=64 · acc=53.1% · units=18.03
- **[B]** `dt-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +24.3%** · n=62 · acc=58.1% · units=15.05

### Japan J1

_League id:_ `J-1-Japan-01` · **3** healthy edges · best ROI **+31.0%**

- **[D]** `svm-result` · `2-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +31.0%** · n=45 · acc=57.8% · units=13.96
- **[C]** `lr-result` · `2-[3.51,100]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +26.1%** · n=50 · acc=66.0% · units=13.04
- **[B]** `svm-result` · `2-[3.51,100]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +23.7%** · n=64 · acc=65.6% · units=15.19

### Mexico Liga MX

_League id:_ `Liga-MX-Mexico-01` · **4** healthy edges · best ROI **+28.1%**

- **[A]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +28.1%** · n=83 · acc=54.2% · units=23.29
- **[B]** `xgb-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +26.9%** · n=73 · acc=54.8% · units=19.66
- **[D]** `dt-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +25.0%** · n=44 · acc=59.1% · units=11.0
- **[B]** `rf-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +22.6%** · n=72 · acc=55.6% · units=16.24

### Denmark Superliga

_League id:_ `Super-Liga-Denmark-01` · **2** healthy edges · best ROI **+27.2%**

- **[D]** `lr-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +27.2%** · n=43 · acc=53.5% · units=11.7
- **[D]** `rf-result` · `2-[3.51,100]` · p=`{"p1":0,"px":0,"p2":20}` · **ROI +21.0%** · n=45 · acc=73.3% · units=9.44

### Norway Eliteserien

_League id:_ `Eliteserien-Norway-01` · **3** healthy edges · best ROI **+26.8%**

- **[D]** `rf-result` · `2-[2.5,3.5]` · p=`{"p1":10,"px":10,"p2":10}` · **ROI +26.8%** · n=49 · acc=53.1% · units=13.12
- **[D]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +23.7%** · n=49 · acc=51.0% · units=11.63
- **[D]** `xgb-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +21.7%** · n=49 · acc=51.0% · units=10.65

### Portugal Liga 1

_League id:_ `Liga-1-Portugal-01` · **3** healthy edges · best ROI **+26.6%**

- **[D]** `dt-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":20,"p2":0}` · **ROI +26.6%** · n=45 · acc=57.8% · units=11.98
- **[B]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +24.5%** · n=61 · acc=47.5% · units=14.95
- **[D]** `xgb-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":0,"p2":40}` · **ROI +22.9%** · n=49 · acc=49.0% · units=11.21

### Switzerland Super League

_League id:_ `Super-League-Switzerland-01` · **2** healthy edges · best ROI **+26.0%**

- **[D]** `xgb-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +26.0%** · n=40 · acc=67.5% · units=10.4
- **[D]** `xgb-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +24.5%** · n=45 · acc=55.6% · units=11.03

### Belgium Jupiler

_League id:_ `Jupiler-League-Belgium-01` · **2** healthy edges · best ROI **+24.6%**

- **[B]** `rf-result` · `1-[2.5,3.5]` · p=`{"p1":30,"px":0,"p2":0}` · **ROI +24.6%** · n=63 · acc=52.4% · units=15.48
- **[D]** `svm-result` · `2-[2.5,3.5]` · p=`{"p1":0,"px":30,"p2":0}` · **ROI +23.6%** · n=45 · acc=48.9% · units=10.63

### England Championship

_League id:_ `Championship-England-01` · **2** healthy edges · best ROI **+23.4%**

- **[D]** `rf-result` · `1-[1.61,1.9]` · p=`{"p1":0,"px":0,"p2":30}` · **ROI +23.4%** · n=49 · acc=69.4% · units=11.44
- **[C]** `xgb-result` · `1-[3.51,100]` · p=`{"p1":30,"px":0,"p2":0}` · **ROI +20.8%** · n=51 · acc=47.1% · units=10.6

### England League Two

_League id:_ `League-2-England-01` · **1** healthy edges · best ROI **+22.6%**

- **[D]** `xgb-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":40,"p2":0}` · **ROI +22.6%** · n=46 · acc=54.3% · units=10.41

### Ireland Premier

_League id:_ `Premier-Division-Ireland-01` · **1** healthy edges · best ROI **+20.6%**

- **[D]** `svm-result` · `1-[1.91,2.5]` · p=`{"p1":0,"px":10,"p2":0}` · **ROI +20.6%** · n=43 · acc=48.8% · units=8.87

## Recurring themes

- **Away [2.5,3.5]** — 20 edges, avg ROI +29.1% · seen in: Belgium Jupiler, Brazil Serie A, Denmark Superliga, England Premier League, France Ligue 1, France Ligue 2, Greece Super League, Mexico Liga MX
- **Home [2.5,3.5]** — 19 edges, avg ROI +32.3% · seen in: Belgium Jupiler, Brazil Serie A, China Super League, England Premier League, Greece Super League, Italy Serie A, Russia Premier League, Scotland Premiership
- **Away [1.91,2.5]** — 16 edges, avg ROI +39.4% · seen in: Argentina Primera, China Super League, France Ligue 2, Italy Serie A, Japan J1, Scotland Premiership, Spain La Liga, Spain Segunda
- **Home [1.91,2.5]** — 15 edges, avg ROI +26.5% · seen in: Brazil Serie A, England League Two, England Premier League, France Ligue 2, Greece Super League, Ireland Premier, Mexico Liga MX, Norway Eliteserien
- **Away [3.51,100]** — 8 edges, avg ROI +25.4% · seen in: Denmark Superliga, Germany Bundesliga 2, Italy Serie A, Japan J1, Russia Premier League
- **Home [1.61,1.9]** — 7 edges, avg ROI +28.6% · seen in: England Championship, Germany Bundesliga 2, Scotland Premiership, Switzerland Super League
- **Draw [2.0,3.0]** — 4 edges, avg ROI +28.0% · seen in: France Ligue 2, Romania Liga 1
- **Home [3.51,100]** — 3 edges, avg ROI +33.7% · seen in: Argentina Primera, England Championship, France Ligue 1
- **Home [1.31,1.6]** — 2 edges, avg ROI +21.8% · seen in: Spain La Liga

## Suggested staking order

1. Trade Tier **A** then **B** first (sample support).
2. Within a tier, prefer higher **n** over slightly higher ROI.
3. Cap exposure on Tier **D** until you have live tracking.
4. Re-run `scripts/research_sweep.py` after league updates; retire edges that decay.

## Skip / weak

- **MLS-USA-01** — research produced 0 candidates (dirty odds with literal `x`).
- Edges with ROI ≤ 20% intentionally omitted from this playbook.

---

_Machine-readable companion:_ see `data/research/playbook-healthy.json`.
