# Running the DILIrank endpoint

DILIrank is a list of drugs ranked by their liver-injury concern in humans, published by FDA (Chen et al., 2016). It is not redistributed here.

1. Download the DILIrank spreadsheet from FDA's Liver Toxicity Knowledge Base page and note its path.
2. Resolve drug names to structures and write the label file:
   `python scripts/prepare_dilirank.py path/to/DILIrank.xlsx`
   This writes `data_raw/dilirank.csv` and lists unresolved drug names in `data_raw/dilirank_unresolved.csv`.
3. Featurise and run the benchmark as usual:
   `python scripts/prepare_data.py data_raw` then `python scripts/run_benchmark.py 0 1 3`

Labels: Most-DILI-concern and Less-DILI-concern are positive, No-DILI-concern is negative, and Ambiguous drugs are removed. Planned: report results with and without the ambiguous drugs.

No DILIrank result is reported in this repository until this run has been done and its outputs are committed.
