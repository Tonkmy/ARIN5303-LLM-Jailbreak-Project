# Guide For Member 3: Defense, Evaluation, and Report Owner

## Your Mission
Build the two defense modules, the evaluation script, and the reporting outputs.

You own:
- `defenses/input_guard.py`
- `defenses/output_guard.py`
- `src/evaluate_results.py`
- summary tables and charts
- first report draft and slide draft

## What You Are Not Responsible For
- Do not run the official full matrix unless the lead asks
- Do not change the dataset schema
- Do not change model endpoint settings on your own

## Files You Must Read First
1. `docs/PROJECT_PLAN.md`
2. `templates/result_record_example.json`
3. `defenses/input_guard.py`
4. `defenses/output_guard.py`
5. `src/evaluate_results.py`

## Required Defense Scope
Keep it simple.
Implement only these 2 required defenses.

### Defense 1: Input Guard
Goal:
- inspect the prompt before it reaches the model

Minimum expected behavior:
- return `blocked = true/false`
- return a short reason string

Suggested first version:
- rule-based detection for obvious override or jailbreak patterns
- optional category-specific heuristics

### Defense 2: Output Guard
Goal:
- inspect the model response after generation

Minimum expected behavior:
- return `blocked = true/false`
- return a short reason string

Suggested first version:
- simple refusal / unsafe marker checks
- optional safety classifier wrapper if available

## Required Interfaces
### input_guard.py
Implement a function with this shape:
```python
def check_input(prompt: str) -> dict:
    return {
        "blocked": False,
        "reason": ""
    }
```

### output_guard.py
Implement a function with this shape:
```python
def check_output(response: str) -> dict:
    return {
        "blocked": False,
        "reason": ""
    }
```

### evaluate_results.py
It must be able to compute at least:
- ASR by defense
- ASR by category
- benign refusal rate by defense
- average latency by defense

## Step-By-Step Work
### Step 1: Implement defense stubs
Fill `defenses/input_guard.py` and `defenses/output_guard.py`.
Keep logic readable and small.

### Step 2: Build local tests
Create a few manual examples in comments or a tiny helper block so the lead can sanity check quickly.

### Step 3: Implement evaluation script
Make `src/evaluate_results.py` read result files and print a compact summary table.
If possible, also write summary CSV files under `results/summary/`.

### Step 4: Define the final figures
You must produce 3 visuals:
1. ASR by defense setting
2. ASR by attack category
3. benign refusal rate by defense setting

### Step 5: Draft report outline
Create `docs/report_outline.md` with these sections:
- Introduction
- Threat model
- Attack categories
- Defenses
- Experimental setup
- Results
- Discussion and limitations
- Conclusion

### Step 6: Draft slide outline
Create `docs/slide_outline.md` with 8 to 10 slides maximum.

## Handoff Checklist
You are done only if all are true:
- [ ] input guard works with the required function signature
- [ ] output guard works with the required function signature
- [ ] evaluation script prints the required metrics
- [ ] report outline exists
- [ ] slide outline exists

## If You Get Stuck
Ask the lead only about:
- final field names in result files
- where official results are stored
- whether a defense should block or only tag

Do not redesign the whole pipeline.
