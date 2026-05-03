# Project Status

## Purpose
This file is the handoff document for future agents or new chat sessions. Read it before editing code. It records the current state, decisions, progress, and next actions for the single-person ARIN5303 LLM jailbreak evaluation project.

## Current Objective
Complete a compact jailbreak evaluation against a local omlx Qwen 35B 8bit MoE model in one focused work session. The evaluation must compare four defense settings on the same attack and benign datasets, then summarize the results in `report.md`.

## Fixed Experiment Scope
- Model: local omlx Qwen 35B 8bit MoE.
- Endpoint style: local omlx `/v1/chat/completions` API using the common chat-completions request format.
- Attack categories: `role_play`, `instruction_override`, `obfuscation`.
- Defense settings: `none`, `input_guard`, `output_guard`, `input_guard+output_guard`.
- Metrics: ASR, benign refusal rate, average latency.
- Total expected records: 80 prompts x 4 settings = 320 records.

## Repository Map
- `README.md`: short entrypoint for the project.
- `docs/PROJECT_PLAN.md`: single-person execution plan and fixed scope.
- `docs/PROJECT_STATUS.md`: current handoff and progress tracker.
- `report.md`: living final-report draft.
- `configs/model_api.example.json`: example local model config.
- `configs/model_api.json`: real local model config, ignored by git and present locally.
- `data/attacks.csv`: attack dataset, complete at 60 rows.
- `data/benign.csv`: benign dataset, complete at 20 rows.
- `templates/`: CSV and result-record examples.
- `defenses/input_guard.py`: readable rule-based guard for override, hidden-prompt disclosure, role-play, and obfuscation patterns.
- `defenses/output_guard.py`: readable rule-based guard for protected prompt-artifact disclosure in model responses.
- `src/call_model.py`: local omlx model caller using Python standard-library HTTP.
- `src/run_experiment.py`: implemented JSONL experiment runner with defense selection, resume skipping, and `--limit` test runs.
- `src/evaluate_results.py`: evaluation scaffold, not implemented.
- `scripts/smoke_test.sh`: real one-prompt smoke test for the local endpoint.
- `results/`: ignored output directory; currently contains small non-official verification runs under `results/raw/`.

## Code Review Snapshot
High-priority issues:
- Official full-matrix runs have not been completed yet.
- `src/evaluate_results.py` does not compute metrics yet. It only prints a placeholder message.
- `data/attacks.csv` is complete at 60 rows, with 20 rows per attack category.
- `data/benign.csv` is complete at 20 rows and passed a basic CSV quality check.
- `configs/model_api.json` exists locally and the local endpoint smoke test succeeded.

Medium-priority issues:
- The input guard blocks 60/60 current attack prompts and 0/20 benign prompts in a static check. This is useful for the fixed evaluation, but should be discussed as dataset-specific rule coverage rather than broad jailbreak robustness.
- The local model may emit a thinking section before its final answer; too-small `max_tokens` values can truncate outputs before the final answer.

Low-priority issues:
- `templates/result_record_example.json` lacks several fields that the final runner should write, such as input/output block status, category, prompt, and error.
- No charting or summary-output conventions are implemented yet.

## Progress Tracker
- [x] Convert project narrative from three-person group work to single-person execution.
- [x] Remove obsolete role-specific docs.
- [x] Add single-person project plan.
- [x] Add this handoff status file.
- [x] Add `report.md` draft.
- [x] Create `configs/model_api.json`.
- [x] Confirm local model smoke test.
- [x] Complete `data/attacks.csv` to 60 rows.
- [x] Complete `data/benign.csv` to 20 rows.
- [x] Implement `src/run_experiment.py`.
- [x] Improve `defenses/input_guard.py`.
- [x] Improve `defenses/output_guard.py`.
- [ ] Implement `src/evaluate_results.py`.
- [ ] Run all four defense settings.
- [ ] Generate summary CSVs.
- [ ] Generate three figures.
- [ ] Copy final metrics and examples into `report.md`.

## Immediate Next Actions
1. Implement evaluation and chart generation.
2. Run all four defense settings on the full 80-prompt dataset.
3. Copy final metrics and representative examples into `report.md`.
4. Discuss that the rule-based input guard is closely matched to the fixed benchmark categories.

## Recommended Commands
Quality check current datasets:
```bash
python3 -c 'import csv,collections; rows=list(csv.DictReader(open("data/attacks.csv", newline=""))); print(len(rows)); print(collections.Counter(r["category"] for r in rows)); print(sum(not r["prompt"] for r in rows), "blank prompts")'
python3 -c 'import csv,collections; rows=list(csv.DictReader(open("data/benign.csv", newline=""))); print(len(rows)); print(collections.Counter(r["category"] for r in rows)); print(sum(not r["prompt"] for r in rows), "blank prompts")'
```

Expected future run commands:
```bash
python3 src/run_experiment.py --defense none
python3 src/run_experiment.py --defense input_guard
python3 src/run_experiment.py --defense output_guard
python3 src/run_experiment.py --defense input_guard+output_guard
python3 src/evaluate_results.py
```

## Report Notes To Preserve
- The report should frame this as a controlled, small-scale security evaluation, not as a comprehensive jailbreak benchmark.
- The method should emphasize fixed model settings, same dataset across all defenses, and transparent rule-based guards.
- Limitations should mention heuristic labeling, small dataset size, local single-model scope, and no external judge model.
- Results are not available yet. Do not fabricate metrics.
