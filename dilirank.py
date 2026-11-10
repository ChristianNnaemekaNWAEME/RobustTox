"""Loader for the FDA DILIrank list (drug-induced liver injury concern).

The list is downloaded by the user from the FDA website and is not bundled.
Column names follow the published DILIrank spreadsheet; they are matched
case-insensitively so small header changes do not break loading.
"""
import pandas as pd

_CANON = {"compoundname": "name", "ltkbid": "ltkb_id",
          "severityclass": "severity", "labelsection": "label_section",
          "vdili-concern": "concern", "vdili concern": "concern",
          "comment": "comment"}
CONCERN_TO_LABEL = {"most-dili-concern": 1, "less-dili-concern": 1,
                    "no-dili-concern": 0}  # 'ambiguous' is dropped


def load_dilirank(path):
    """Read a DILIrank .xlsx/.csv file into a tidy frame with a binary label."""
    df = (pd.read_excel(path, header=None) if str(path).endswith("xlsx")
          else pd.read_csv(path, header=None))
    # the published sheet has title rows; find the header row
    hdr = next(i for i in range(min(10, len(df)))
               if df.iloc[i].astype(str).str.lower().str.contains("compound").any())
    df.columns = [str(c).strip().lower() for c in df.iloc[hdr]]
    df = df.iloc[hdr + 1:].reset_index(drop=True)
    df = df.rename(columns={c: _CANON[c] for c in df.columns if c in _CANON})
    if "concern" not in df or "name" not in df:
        raise ValueError("DILIrank file is missing compound name or concern column")
    df["concern"] = df["concern"].astype(str).str.strip().str.lower()
    df["label"] = df["concern"].map(CONCERN_TO_LABEL)
    return df.dropna(subset=["label"]).astype({"label": int})
