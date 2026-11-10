# RobustTox: Work in Progress (Phase 1)

Last updated: November 5, 2026

This file records the work now under way and what is not yet done. **No results from the items below are reported anywhere in this repository yet.** Results will be added to `results/` and the report only when the code, splits and tests for them are public.

## Phase 1 (current): extend the toxicity study

| Item | Status |
|---|---|
| Add FDA's DILIrank list (drugs ranked by liver-injury concern) as a new endpoint | In progress: loader, data-preparation script, tests and run instructions are in `phase1-dilirank`; the benchmark run is not done |
| Add further Tox21 and ToxCast endpoints | In progress |
| Compare against a published graph neural network | In progress |
| Tune every comparison model fairly (Random Forest, gradient boosting, L1 logistic regression) | In progress |
| Build a robust starting point for the trimming algorithm | In progress |
| Report results with and without ambiguous labels | Planned |
| Public release of code, data splits and results, and a paper submission | Planned |

## Later phases (planned, not started)

* **Phase 2:** contamination taken from real label conflicts between databases, outlying descriptors and mislabelled batches, evaluation on later drugs, and review of selected substructures by toxicologists.
* **Phase 3:** more safety endpoints, context-of-use documentation, and maintained repositories.

## What is already done

See `README.md` and `docs/report/RobustTox_Technical_Report.pdf`: a 17-endpoint benchmark with three tested repairs, a simulation study and a theory note. The current benchmark does not include DILIrank, and its ToxCast endpoints are in-vitro readouts, not clinical liver injury.

## How to follow progress

Commits and branches for this work are public. The branch `phase1-dilirank` holds the liver-injury work until it is ready to merge.
