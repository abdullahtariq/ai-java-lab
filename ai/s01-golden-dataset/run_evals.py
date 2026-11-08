import json
import pathlib

from google import genai

from checks import EVALS
from summarizer import MODEL, summarize

HERE = pathlib.Path(__file__).parent

# load the golden dataset
lines = (HERE / "golden.jsonl").read_text(encoding="utf-8").splitlines()
cases = [json.loads(l) for l in lines if l.strip()]

client = genai.Client()
results = []
passed_checks = total_checks = passed_cases = 0

# get a summary then ask every eval its question
for case in cases:
    output = summarize(case["input"], client)
    case_ok = True
    print(f"\n{case['id']}: {case['why']}")
    for ev in EVALS:
        result, details = ev(output, case)
        if result is None:
            print(f" n/a {ev.__name__}")
            continue
        total_checks += 1
        passed_checks += result
        case_ok = case_ok and result
        print(f"  {'PASS' if result else 'FAIL'}  {ev.__name__}: {details}")
    
    if not case_ok:
        print(f" output: {output}")
    passed_cases += case_ok
    results.append({"id": case["id"], "model": MODEL, "output": output, "passed": case_ok})

# Scoring
print(f"\nCases passed: {passed_cases}/{len(cases)}")
print(f"\nCheck passed: {passed_checks}/{total_checks}")

# Save outputs so later sessions can reuse it
out = "".join(json.dumps(r) + "\n" for r in results)
(HERE / "results.jsonl").write_text(out, encoding="utf-8")