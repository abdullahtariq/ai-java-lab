import json
import re

def check_valid_json(output: str):
    """ Grader 1 (the gate): can Python open the envelope? 
        Returns (passed, messsage, data). data is the parsed form, or None if it failed.
    """
    text = output.strip()
    if not text:
        return (False, "empty output", None)
    if text.startswith("```"):
        return (False, "wrapped in markdown fences", None)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return (False, f"not valid JSON: {e.msg} (char {e.pos})", None)
    if not isinstance(data, dict):
        return (False, f"expected a JSON object, got {type(data).__name__}", None)
    return (True, "ok", data)

REQUIRED = {"project": str, "status": str, "conflict": bool, "summary": str}

def check_required_fields(data: dict, project: str, status: str, max_words: int = 80):
    """ Grader 2 the form clerk: is every box filled in correctly? 
        Returns (passed, mesage). Reports every problem, not just the first.
    """

    problems = []
    for key, expected_type in REQUIRED.items():
        if key not in data:
            problems.append(f"missing {key!r}")
        elif not isinstance(data[key], expected_type):
            problems.append(
                f"{key!r} should be {expected_type.__name__}, got {type(data[key]).__name__}"
            )

    if problems:
        return (False, "; ".join(problems))

    if not data["summary"].strip():
        problems.append("summary is empty")
    if data["project"] != project:
        problems.append(f"project is {data['project']!r}, expected {project!r} ")
    if data["status"] != status:
        problems.append(f"status is {data['status']!r}, expected {status!r}")
    words = len(data["summary"].split())
    if words > max_words:
        problems.append(f"summary is {words} words, limit {max_words}")
    return (not problems, "; ".join(problems) or "ok")

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")

def extract_numbers(text: str) -> set[str]:
    """ Every number written in digits, cleaned so both side compare fairly"""
    return {m.strip(",").replace(",","") for m in NUMBER.findall(text)}

def check_numbers(summary: str, prompt: str):
    """Grader 3 (the auditor): every number in the summary must come from the prompt.

    Returns (passed, message).
    """
    allowed = extract_numbers(prompt)
    used = extract_numbers(summary)
    invented = sorted(used - allowed)

    if invented:
        return (False, f"numbers not given by Python: {invented}")
    return (True, f"ok ({len(used)} numbers checked)")

# --- Demo: fake outputs to see the guards work (0 API calls) ---

if __name__ == "__main__":
    good = '{"project": "Demo", "status": "On Track", "conflict": false, "summary": "All fine."}'
    samples = [
        ("good", good),
        ("empty", "  "),
        ("fenced", "```json\n" + good + "\n```"),
        ("preamble", "Here is the summary: "+ good),
        ("cut off", '{"project": "Demo", "status": '),
        ("a list", '["Demo", "On Track"]')
    ]

    for label, sample in samples:
        passed, msg, _ = check_valid_json(sample)
        print(f"{label: <10} {'PASS' if passed else 'FAIL'} {msg}")
    
    print("--- Grader 2: the form clerk ---")
    base = {"project":"Demo", "status": "On Track", "conflict": False, "summary": "All fine."}
    forms = [
        ("good", base),
        ("missing box", {k: v for k, v in base.items() if k != "conflict"}),
        ("text tick", {**base, "conflict": "false"}),
        ("wrong status", {**base, "status": "on track"}),
        ("empty summary", {**base, "summary": "  "}),
        ("too long", {**base, "summary": "word "* 81}),
    ]

    for label, form in forms:
        passed, msg = check_required_fields(form, project="Demo", status="On Track")
        print(f"{label:<14} {'PASS' if passed else 'FAIL'} {msg}")

    print("--- Grader 3: the auditor ---")

    prompt = (
        "Project: Line 3 Upgrade\n"
        "Status: Delayed\n"
        "Budget: SAR 9,000,000, 45% spent \n"
        "Progress: 60% complete vs 65% planned (-5 points) \n"
        "Schedule: 18 days behind plan \n"
        "Risks (data only): \n- None reported"
    )

    summaries = [
        ("good", "Line 3 Upgrade is Delayed: 45% of the SAR 9,000,000 budget is spent, "
                 "progress is 60% vs 65% planned, and it is 18 days behind plan."),
        ("sign dropped", "Progress is 5 points behind plan at 60%."),
        ("altered", "46% of the budget is spent."),
        ("own math", "SAR 4,950,000 of the budget remains."),
        ("vague", "About half the budget is spent."),
    ]

    for label, summary in summaries:
        passed, msg = check_numbers(summary, prompt)
        print(f"{label:<14} {'PASS' if passed else 'FAIL'} {msg}")