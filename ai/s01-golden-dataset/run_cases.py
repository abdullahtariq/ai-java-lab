import json
import pathlib

from google import genai
from summarizer import build_prompt, summarize

HERE = pathlib.Path(__file__).parent

cases = []

# Load the golden dataset 
for line in (HERE / "golden.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        cases.append(json.loads(line))

# creating the genai client    
client = genai.Client()

# for each case : show what the model was given, then what it wrote
for case in cases:
    print("=" * 70)
    print(f"{case['id']}: {case['why']}")
    print("------------prompt the model recieved-------------")
    print(build_prompt(case["input"]))
    print("---- model output ----")
    print(summarize(case["input"], client))
print("=" * 70)