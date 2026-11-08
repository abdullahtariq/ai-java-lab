"""Session 1: code-based evals. Each eval asks ONE yes/no question about a summary."""

import json
import pathlib

CONFLICT_WORDS = ["conflict", "contradict", "does not match", "doesn't match", "inconsistent", "mismatch"]

def conflict_flagged(output: str, case: dict):
    """ If the case expects a conflict, the summary must mention it. """
    if not case["expect"].get("expects_conflict"):
        return None, "n/a"
    text = output.lower()
    found = [w for w in CONFLICT_WORDS if w in text]

    if found:
        return True, f"flagged: {found}"
    return False, "conflict expected but not mentioned"

def facts_present(output: str, case: dict):
    """ Eval 1: does the summary include every must-say item? """
    text = output.lower()
    missing = [s for s in case["expect"]["must_include"] if s.lower() not in text]
    return (not missing, f"missing: {missing}" if missing else "ok")

def no_false_claims(output: str, case: dict):
    """Eval 2: does the summary avoid every must-never-say phrase?"""
    text = output.lower()
    found = [s for s in case["expect"]["must_not_include"] if s.lower() in text]
    return (not found, f"found: {found}" if found else "ok")

def no_invented_conflict(output: str, case: dict):
    """Eval 4: if this case has no real conflict, the summary must not claim one."""
    if case["expect"].get("expects_conflict", False):
        return (None, "n/a: this case has a real conflict")
    text = output.lower()
    found = [w for w in CONFLICT_WORDS if w in text]
    return (not found, f"claims conflict: {found}" if found else "Ok")

EVALS = [facts_present, no_false_claims, no_invented_conflict, conflict_flagged]

if __name__ == "__main__":
    path = pathlib.Path(__file__).parent / "golden.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    cases = {c["id"]: c for c in (json.loads(l) for l in lines if l.strip())}
    c06 = cases["c06"]

    good = ("New Corniche - Dammam is At Risk: 55% complete against 60% planned "
            "and 5 days behind, with 50% of the budget spent.")
    bad = ("New Corniche - Dammam is At Risk with 50% spent and 5 days behind. "
           "A conflict exists because no risks are listed.")

    for label, text in [("GOOD summary", good), ("BAD summary", bad)]:
        print(label, "label")
        for ev in EVALS:
            result, detail = ev(text, c06)
            mark = "n/a " if result is None else ("PASS" if result else "FAIL")
            print(f" {mark} {ev.__name__} : {detail}")