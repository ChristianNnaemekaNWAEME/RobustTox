import pandas as pd
from robusttox.dilirank import load_dilirank


def test_load_dilirank_csv(tmp_path):
    rows = [["DILIrank", "", ""], ["LTKBID", "CompoundName", "vDILI-Concern"],
            ["LT1", "drugA", "Most-DILI-concern"],
            ["LT2", "drugB", "No-DILI-concern"],
            ["LT3", "drugC", "Ambiguous DILI-concern"]]
    p = tmp_path / "d.csv"
    pd.DataFrame(rows).to_csv(p, header=False, index=False)
    out = load_dilirank(p)
    assert list(out["name"]) == ["drugA", "drugB"]
    assert list(out["label"]) == [1, 0]
