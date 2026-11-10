# Paper outline (working title: "When does robust sparse estimation help? A contamination benchmark for toxicity prediction")

## Honest summary of what the data show (17 endpoints, 3 scaffold splits each; mean ROC-AUC, 95% bootstrap CI over endpoints)

| Condition | L1-Logit | earlier estimator (SLTS-linear) | AdaTrim | RobustTox | Random Forest |
|---|---|---|---|---|---|
| clean labels | 0.751 [0.720, 0.782] | 0.726 [0.701, 0.751] | 0.754 [0.723, 0.785] | 0.738 [0.707, 0.767] | 0.797 [0.767, 0.827] |
| 20% random flips | 0.685 [0.657, 0.712] | 0.686 [0.658, 0.713] | 0.683 [0.658, 0.710] | 0.668 [0.640, 0.699] | 0.719 [0.693, 0.748] |
| 20% margin flips | 0.432 [0.371, 0.497] | 0.390 [0.334, 0.448] | 0.429 [0.364, 0.494] | 0.426 [0.359, 0.491] | 0.646 [0.617, 0.679] |

1. **The fix worked against the earlier estimator, not against the simple baseline.** AdaTrim beats the earlier estimator by +0.028 AUC on clean labels (15/17 endpoints, Wilcoxon p=0.0002) and by +0.03 to +0.04 under margin flips (p=0.01–0.03), and is statistically indistinguishable from plain L1-logistic regression in every condition. No trimming variant is significantly better than L1-Logit in any condition.
2. **Random label flips are survivable for everyone, as Proposition 4 predicts.** AUC falls by 0.03 (10%), 0.07 (20%), 0.12 (30%) for plain L1 and the trimmed variants alike. The earlier estimator loses least (0.040 at 20%) only because it starts lower; its AUC is not different from L1-Logit's at any noise level.
3. **Worst-case (margin) flips destroy every linear model** (AUC at or below chance at 20%) **while Random Forest and gradient boosting keep 0.65.** Trimming does not rescue the linear models because it cannot find the flipped records (3–8% recovered, no better than chance).
4. **Trimming identifies contaminated labels only weakly on real data:** under random flips it removes flipped labels 1.2–1.7 times more often than chance (17–20% of flips removed while trimming 10–15% of records); under margin flips it removes them *less* often than chance (0.4–0.8 times).
5. **Sparsity:** RobustTox and stability selection keep a median of 8 features on clean labels (5–26 across all conditions) against 38 on clean labels (65–121 under contamination) for L1-Logit, at a cost of 0.013 (RobustTox) to 0.024 (StabSel) AUC on clean labels. Selection stability across splits (Jaccard) is 0.45 (RobustTox) and 0.54 (StabSel) against 0.45 (L1-Logit) on clean labels, and *no better than L1-Logit under 20% random noise* (0.12 against 0.13).
6. **Interpretability:** the toxic-associated Morgan bits chosen by L1-Logit and RobustTox overlap Brenk/PAINS/NIH alert atoms *no more than random bits of similar frequency* (mean difference −0.035 and −0.059; no endpoint significant at 0.05; Fisher combined p≈1). A model using only the alert flags reaches AUC 0.594 against 0.751 for the fingerprint model. One mechanistically sensible example: for Tox21 SR-ARE (an electrophile-stress response) the top selected bit is a C=C environment that overlaps the Brenk Michael-acceptor and NIH acrylate alerts in 61% of molecules that carry it.

## Candidate claims for a paper (each backed by the tables above)
* A reproducible contamination benchmark for toxicity data with two noise models and scaffold splits.
* A negative result: trimmed sparse logistic estimators do not improve over plain L1 under random label noise (explained by Proposition 4), and fail under structured noise because the concentration steps are initialised from a corrupted fit (simulation, THEORY §8).
* A positive, practical result: tree ensembles are far more robust to confident-label flips than any linear model tested.
* Interpretability: learned sparse features are not simply re-discovering standard structural alerts.

## Threats to validity you must address before submitting
* **Margin contamination is built from a reference L1-logistic fit**, so it is deliberately adversarial to linear models; Random Forest's advantage there is partly by construction. Add a contamination model that does not depend on any model family (e.g. flips concentrated on assay-interference compounds, or real cross-database label conflicts, Phase 5).
* Three scaffold splits per endpoint; use 10 for the final paper. Confidence intervals are bootstrap over endpoints, which treats the 12 Tox21 tasks as independent although they share molecules.
* The ToxCast endpoints are in-vitro HepG2 readouts. They are not drug-induced liver injury; add DILIrank when it can be downloaded.
* The SIDER label is a clinical side-effect category, not an assay.
* Hyperparameters (C grid, B=20, pi=0.6, trimming grid) were fixed in advance and not tuned on test data, but they were not optimised either; a stronger tuned baseline could change the picture.
* Morgan counts are folded into 512 bins, so one "bit" can mix environments; the substructure shown is the most frequent one.
* The theory has open items (THEORY §7); do not call anything a theorem that is labelled Claim.

## Suggested structure
1 Introduction · 2 Related work (robust statistics; label noise in cheminformatics; structural alerts) · 3 Methods (estimators, contamination models) · 4 Theory (Props 1–4, limits) · 5 Benchmark · 6 Results · 7 Interpretability · 8 Limitations · 9 Conclusion. Target: a workshop first (e.g. an ML-for-drug-discovery workshop), then *Journal of Cheminformatics* or *Chemical Research in Toxicology* once DILI and a real-noise experiment are in.

## Next experiments, in order
1. Robust initialisation for the concentration steps (the failure in THEORY §8): multi-start from sub-samples, or start from a tree ensemble's out-of-fold predictions.
2. Real contamination: compare labels for the same compounds across Tox21, ToxCast and ChEMBL; treat disagreements as noise.
3. Robust tree ensembles and calibrated ensembles as the main competitor.
4. DILIrank and a hepatotoxicity-specific analysis; ask a toxicologist to review the Phase 4 substructures.
