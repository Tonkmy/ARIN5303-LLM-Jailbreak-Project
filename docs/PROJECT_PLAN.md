# Project Plan

## Scope
Evaluate three jailbreak attack categories against a locally served omlx Qwen 35B 8bit MoE model, then compare baseline, input defense, output defense, and layered defense on attack success rate, benign refusal rate, and latency.

This is now a single-person project. The objective is a course-submission-quality evaluation that can be completed in one focused day if the local model endpoint is stable.

## Fixed Decisions
- Main model: local omlx Qwen 35B 8bit MoE API.
- API style: local omlx `/v1/chat/completions` endpoint using the common chat-completions request format.
- Official attack categories: `role_play`, `instruction_override`, `obfuscation`.
- Official defenses: `input_guard` and `output_guard`.
- Official experiment settings: `none`, `input_guard`, `output_guard`, `input_guard+output_guard`.
- Official metrics: ASR, benign refusal rate, and average latency.
- Scope control: do not add attack categories, model variants, external judges, or extra defense variants until the fixed matrix is complete.

## Deliverables
- `configs/model_api.json`: local endpoint configuration, ignored by git.
- `data/attacks.csv`: 60 attack prompts, exactly 20 per attack category.
- `data/benign.csv`: 20 benign prompts.
- `defenses/input_guard.py`: pre-generation guard with `check_input(prompt: str) -> dict`.
- `defenses/output_guard.py`: post-generation guard with `check_output(response: str) -> dict`.
- `src/call_model.py`: local model client.
- `src/run_experiment.py`: runner for the four official settings.
- `src/evaluate_results.py`: summary metrics and chart generation.
- `results/`: raw JSONL results, summaries, and figures, ignored by git.
- `report.md`: living final-report draft.

## Dataset Plan
Attack dataset:
- 60 rows total.
- 20 rows in `role_play`.
- 20 rows in `instruction_override`.
- 20 rows in `obfuscation`.
- Columns must match `templates/attack_dataset_template.csv`.
- Each row should include `id`, `category`, `source`, `prompt`, `target_behavior`, `is_benign`, and `notes`.

Benign dataset:
- 20 rows total.
- Category must be `benign`.
- Prompt types should cover factual QA, summarization, writing help, simple coding help, and planning help.
- Columns must match `templates/benign_dataset_template.csv`.

## Experiment Matrix
Run exactly these four settings on the same input files:
1. `none`
2. `input_guard`
3. `output_guard`
4. `input_guard+output_guard`

Expected total calls:
- 80 prompts x 4 settings = 320 prompt records.
- Input-guard-blocked records should still be written, with no model response and a recorded block reason.

## Result Schema
Each raw result record should include at least:
- `id`
- `category`
- `is_benign`
- `model`
- `defense`
- `prompt`
- `target_behavior`
- `input_blocked`
- `input_guard_reason`
- `response`
- `output_blocked`
- `output_guard_reason`
- `refused`
- `attack_success`
- `latency_ms`
- `error`

## Metrics
Primary:
- ASR by defense: attack-successful records divided by total attack records for each defense.
- ASR by category: attack-successful records divided by total attack records for each category and defense.
- Benign refusal rate by defense: benign records blocked or refused divided by total benign records for each defense.

Secondary:
- Average latency by defense.
- Error count by defense.

## One-Day Execution Plan
Phase 1: Freeze configuration.
- Create `configs/model_api.json` from the example.
- Confirm the local model endpoint, model name, temperature, max tokens, and timeout.
- Run a one-prompt smoke test.

Phase 2: Complete benchmark files.
- Fill `data/attacks.csv` to 60 rows.
- Fill `data/benign.csv` to 20 rows.
- Run a CSV quality check for counts, blank required fields, duplicate prompts, and category spelling.

Phase 3: Implement pipeline.
- Make `src/run_experiment.py` load CSV rows and run one or all defense settings.
- Make the runner resumable enough to avoid losing completed records after interruption.
- Write raw results under `results/raw/`.

Phase 4: Implement evaluation.
- Make `src/evaluate_results.py` read raw JSONL files.
- Write summary CSV files under `results/summary/`.
- Generate three figures under `results/figures/`.

Phase 5: Finish report.
- Copy final metrics into `report.md`.
- Add representative examples and limitations.
- Record unresolved issues in `docs/PROJECT_STATUS.md`.

## Completion Criteria
The project is complete when:
- The local model configuration is frozen.
- The attack and benign datasets match the required counts.
- All four experiment settings run on the same dataset.
- Raw results, summaries, and three figures exist under `results/`.
- `report.md` explains the strongest attack category, the most useful defense setting, benign refusal tradeoffs, and limitations.
