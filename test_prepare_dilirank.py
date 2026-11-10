import importlib.util, os
spec = importlib.util.spec_from_file_location(
    "prepare_dilirank", os.path.join(os.path.dirname(__file__), "..", "scripts", "prepare_dilirank.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_smiles_from_response_prefers_canonical():
    payload = {"PropertyTable": {"Properties": [{"CID": 1, "ConnectivitySMILES": "CC", "CanonicalSMILES": "CCO"}]}}
    assert mod.smiles_from_response(payload) == "CCO"


def test_smiles_from_response_falls_back():
    payload = {"PropertyTable": {"Properties": [{"CID": 1, "ConnectivitySMILES": "CC"}]}}
    assert mod.smiles_from_response(payload) == "CC"
