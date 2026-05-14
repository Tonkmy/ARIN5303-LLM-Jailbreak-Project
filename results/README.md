# Results Directory

This directory contains local experiment outputs for the completed jailbreak evaluation run.

## Files

- `raw/none.jsonl`: Raw records for the no-defense baseline.
- `raw/input_guard.jsonl`: Raw records for the input-guard setting.
- `raw/output_guard.jsonl`: Raw records for the output-guard setting.
- `raw/input_guard+output_guard.jsonl`: Raw records for the layered defense setting.
- `summary/summary_by_defense.csv`: Overall ASR, benign refusal rate, error count, and average latency by defense.
- `summary/asr_by_category.csv`: ASR split by attack category and defense.
- `summary/latency_by_defense.csv`: Average, median, min, and max latency by defense.
- `figures/asr_by_defense.svg`: Bar chart for ASR by defense.
- `figures/asr_by_category.svg`: Grouped bar chart for ASR by attack category.
- `figures/benign_refusal_by_defense.svg`: Bar chart for benign refusal rate by defense.
- `report.md`: Result-focused report for this experiment run.

## Notes

- The completed run contains 320 raw records: 80 prompts x 4 defense settings.
- No runtime/API errors were recorded in this run.
- Attack success is labeled by the project heuristic in `src/run_experiment.py`.
