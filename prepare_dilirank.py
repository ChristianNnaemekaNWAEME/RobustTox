"""Build data_raw/dilirank.csv (smiles, DILI label) from the FDA DILIrank spreadsheet.

Usage:  python scripts/prepare_dilirank.py PATH_TO_DILIrank.xlsx [out_csv]

DILIrank lists drug names, not structures, so each name is looked up in PubChem
(PUG REST) and the answers are cached in data_raw/dilirank_smiles_cache.csv, which
makes re-runs cheap. Drugs that PubChem cannot resolve are written to
data_raw/dilirank_unresolved.csv instead of being guessed. Ambiguous-concern drugs
are removed (see robusttox/dilirank.py).
"""
import os, sys, time, json, urllib.parse, urllib.request
import pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from robusttox.dilirank import load_dilirank

URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/CanonicalSMILES,ConnectivitySMILES/JSON"
KEYS = ("CanonicalSMILES", "ConnectivitySMILES", "SMILES", "IsomericSMILES")


def smiles_from_response(payload):
    """Pick the first SMILES field of the first compound in a PubChem property answer."""
    props = payload["PropertyTable"]["Properties"][0]
    for k in KEYS:
        if props.get(k):
            return props[k]
    return None


def lookup(name, retries=2):
    for a in range(retries + 1):
        try:
            with urllib.request.urlopen(URL.format(urllib.parse.quote(name)), timeout=30) as r:
                return smiles_from_response(json.load(r))
        except Exception:
            time.sleep(1 + a)
    return None


def main(src, out=None):
    raw = os.path.join(ROOT, "data_raw"); os.makedirs(raw, exist_ok=True)
    out = out or os.path.join(raw, "dilirank.csv")
    cache_f = os.path.join(raw, "dilirank_smiles_cache.csv")
    cache = dict(pd.read_csv(cache_f).values) if os.path.exists(cache_f) else {}
    df = load_dilirank(src)
    for name in df["name"]:
        if name not in cache:
            cache[name] = lookup(name) or ""
            time.sleep(0.25)  # stay under PubChem's request limit
            pd.DataFrame(list(cache.items()), columns=["name", "smiles"]).to_csv(cache_f, index=False)
    df["smiles"] = df["name"].map(cache)
    ok = df["smiles"].astype(str).str.len() > 0
    df[~ok][["name", "concern"]].to_csv(os.path.join(raw, "dilirank_unresolved.csv"), index=False)
    df[ok].rename(columns={"label": "DILI"})[["name", "smiles", "DILI", "concern"]].to_csv(out, index=False)
    print(f"{ok.sum()} of {len(df)} drugs resolved; positives {int(df[ok]['label'].sum())}; written to {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
