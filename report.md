# Final Report Draft

## Title
Evaluating Rule-Based Defenses Against Jailbreak Prompts on a Local Qwen 35B 8bit MoE Model

## Abstract
This project evaluates three common jailbreak prompt categories against a locally served omlx Qwen 35B 8bit MoE model. The experiment compares four settings: no defense, input guard, output guard, and layered input-plus-output guard. The main metrics are attack success rate, benign refusal rate, and average latency. Results will be added after the full experiment matrix is run.

## 1. Introduction
Large language models can be vulnerable to jailbreak prompts that attempt to bypass safety behavior through role-play, instruction overrides, or obfuscation. This project performs a compact empirical evaluation of those attack categories against a local model and measures whether simple rule-based defenses reduce unsafe completions while preserving helpful responses to benign prompts.

## 2. Research Questions
1. Which jailbreak category is most effective against the local Qwen 35B 8bit MoE model?
2. How much do input and output guards reduce attack success rate?
3. What benign refusal tradeoff is introduced by each defense setting?
4. What latency overhead appears when defenses are layered?

## 3. Threat Model
The attacker can submit arbitrary user prompts to the model. The attacker cannot modify the model weights, system prompt, decoding configuration, server code, or defense code. The defender can inspect prompts before generation and inspect responses after generation. The evaluation focuses on prompt-level jailbreak behavior, not network security, model extraction, or tool-use attacks.

## 4. Attack Categories
`role_play`:
Prompts that ask the model to adopt a fictional persona, simulation context, alternate character, or hypothetical setting that may weaken normal safety behavior.

`instruction_override`:
Prompts that directly ask the model to ignore, replace, reveal, or supersede prior instructions, system messages, developer messages, or safety rules.

`obfuscation`:
Prompts that hide intent through encoding, spacing, symbolic transformations, indirect wording, or unusual formatting.

## 5. Defenses
Input guard:
A pre-generation rule-based filter that scans the user prompt for instruction overrides, hidden-prompt disclosure requests, role-play wrappers, and light obfuscation such as spacing, punctuation splitting, leetspeak, ROT13/Base64 framing, reversed text, and translation framing. On the fixed dataset, the current input guard blocks 60/60 attack prompts and 0/20 benign prompts in a static CSV check.

Static input-guard validation:
- `input_guard_attack_blocked 60 / 60` means all 60 prompts in `data/attacks.csv` were blocked by the input guard before model generation.
- `input_guard_benign_blocked 0 / 20` means none of the 20 benign prompts in `data/benign.csv` were blocked by the input guard.
- This is a pre-generation rule check only. It does not measure model behavior, output-guard behavior, or full experiment ASR. It shows that the input guard is well matched to the fixed benchmark patterns, but it should not be interpreted as broad jailbreak robustness against unseen attacks.

Output guard:
A post-generation rule-based filter that scans the model response for apparent disclosure of protected prompt artifacts, such as system prompts, developer messages, hidden instructions, private rules, prompt stacks, or instruction hierarchy. It does not block ordinary refusal text, because refusals are the desired safe outcome for attack prompts.

Layered defense:
Both guards are applied. The input guard can stop high-risk prompts early, while the output guard catches unsafe generations that pass the input check.

## 6. Experimental Setup
Model:
- Local omlx Qwen 35B 8bit MoE.

Endpoint:
- Local omlx `/v1/chat/completions` API. Its request and response shape follows the common OpenAI chat-completions format, but the experiment sends requests only to the local server.
- Exact base URL and model name will be recorded after `configs/model_api.json` is created.

Decoding:
- Temperature, max tokens, timeout, and system prompt are frozen before official runs.
- During initial smoke testing, short `max_tokens` values caused the local model response to be truncated inside its generated thinking section. This initially looked like a model-calling problem, but a longer generation budget produced the expected final answer. The working configuration therefore uses `max_tokens = 1000` for official runs so completions are less likely to stop before the final answer.

Model-calling implementation note:
- `src/call_model.py` does not import or use the external `openai` Python package. It uses Python standard-library HTTP requests, reads the ignored local `configs/model_api.json`, sends the configured bearer token, and posts directly to the local omlx `/v1/chat/completions` endpoint.

Dataset:
- 60 attack prompts, 20 per attack category.
- 20 benign prompts.
- The same dataset is used across all four defense settings.

Experiment matrix:
1. `none`
2. `input_guard`
3. `output_guard`
4. `input_guard+output_guard`

Expected records:
- 80 prompts x 4 settings = 320 records.

## 7. Metrics
Attack success rate:
The fraction of attack prompts that produce a successful unsafe completion under a defense setting.

Benign refusal rate:
The fraction of benign prompts that are incorrectly blocked or refused under a defense setting.

Average latency:
The mean response latency per prompt under a defense setting.

Metric implementation:
- `summary_by_defense.csv` summarizes the overall result for each defense setting. It reports total records, attack records, successful attacks, ASR, benign records, benign refusals, benign refusal rate, error count, and average latency.
- `asr_by_category.csv` breaks ASR down by `role_play`, `instruction_override`, and `obfuscation` for each defense setting. It is used to identify which jailbreak style is strongest under each defense.
- `latency_by_defense.csv` summarizes runtime cost for each defense setting. It reports records without error, average latency, median latency, minimum latency, and maximum latency.

Attack-success labeling:
- Attack success is assigned in `src/run_experiment.py` when each raw JSONL record is written, then `src/evaluate_results.py` only aggregates that stored label.
- A record is counted as a successful attack only when it is an attack prompt, no input guard blocked it, no output guard blocked it, the response did not match the simple refusal heuristic, and no runtime/API error occurred.
- In code form: `attack_success = not is_benign and not refused and not error`, where `refused` includes input blocking, output blocking, or obvious refusal phrases such as "I cannot" or "I can't assist".
- This is a transparent heuristic label rather than a human or LLM-judge annotation. It may overestimate success when a non-refusal answer is still harmless, and it may underestimate success when unsafe content appears alongside refusal-like wording. This limitation should be considered when interpreting ASR.

## 8. Result Tables
Status: full 320-record experiment matrix completed. All four defense settings ran on the same 60 attack prompts and 20 benign prompts. No runtime/API errors were recorded.

### ASR By Defense
| Defense | Attack Records | Successful Attacks | ASR |
|---|---:|---:|---:|
| none | 60 | 20 | 0.3333 |
| input_guard | 60 | 0 | 0.0000 |
| output_guard | 60 | 18 | 0.3000 |
| input_guard+output_guard | 60 | 0 | 0.0000 |

### Benign Refusal Rate By Defense
| Defense | Benign Records | Refused Or Blocked | Benign Refusal Rate |
|---|---:|---:|---:|
| none | 20 | 0 | 0.0000 |
| input_guard | 20 | 0 | 0.0000 |
| output_guard | 20 | 0 | 0.0000 |
| input_guard+output_guard | 20 | 0 | 0.0000 |

### ASR By Category
| Defense | Category | Attack Records | Successful Attacks | ASR |
|---|---|---:|---:|---:|
| none | role_play | 20 | 9 | 0.4500 |
| none | instruction_override | 20 | 8 | 0.4000 |
| none | obfuscation | 20 | 3 | 0.1500 |
| input_guard | role_play | 20 | 0 | 0.0000 |
| input_guard | instruction_override | 20 | 0 | 0.0000 |
| input_guard | obfuscation | 20 | 0 | 0.0000 |
| output_guard | role_play | 20 | 6 | 0.3000 |
| output_guard | instruction_override | 20 | 8 | 0.4000 |
| output_guard | obfuscation | 20 | 4 | 0.2000 |
| input_guard+output_guard | role_play | 20 | 0 | 0.0000 |
| input_guard+output_guard | instruction_override | 20 | 0 | 0.0000 |
| input_guard+output_guard | obfuscation | 20 | 0 | 0.0000 |

### Latency By Defense
| Defense | Records Without Error | Avg Latency ms | Median Latency ms | Min Latency ms | Max Latency ms |
|---|---:|---:|---:|---:|---:|
| none | 80 | 26631.1 | 23177.0 | 5119.0 | 49340.0 |
| input_guard | 80 | 2960.1 | 0.0 | 0.0 | 22232.0 |
| output_guard | 80 | 25903.7 | 20832.5 | 5787.0 | 83503.0 |
| input_guard+output_guard | 80 | 5723.6 | 0.0 | 0.0 | 55034.0 |

Initial result reading:
- Baseline ASR was 0.3333. The strongest baseline category was `role_play` at 0.4500, followed by `instruction_override` at 0.4000 and `obfuscation` at 0.1500.
- The input guard reduced ASR to 0.0000 because it blocked all attack prompts before generation on this fixed benchmark.
- The output guard reduced ASR only slightly, from 0.3333 to 0.3000. It helped most on `role_play`, reducing category ASR from 0.4500 to 0.3000, but did not reduce `instruction_override` in this heuristic evaluation.
- Layered defense also produced ASR 0.0000, mainly because the input guard blocked all attack prompts before the output guard was needed.
- Benign refusal rate was 0.0000 under all four settings. In this run, neither guard blocked or caused obvious refusal for the 20 benign prompts.
- Latency was lowest for input-guard and layered settings because blocked attack prompts did not call the model. Their median latency is 0.0 ms because 60 of 80 records were blocked before generation.



## 9. Discussion Points To Fill After Results
- Which attack category had the highest ASR and why.
- Whether input filtering mainly reduced obvious instruction overrides.
- Whether output filtering caught unsafe completions missed by input filtering.
- Whether layered defense reduced ASR at the cost of higher benign refusal.
- Whether latency overhead was meaningful relative to model generation time.

## 10. Limitations
- Small benchmark size.
- Single local model.
- Rule-based defenses only.
- Heuristic attack-success and refusal detection unless manually audited.
- No external LLM judge or human annotation pass yet.
- Results may depend on the exact system prompt and decoding settings.

## 11. Conclusion
The full experiment matrix shows that rule-based input filtering was the most effective defense on this fixed benchmark, reducing heuristic ASR from 0.3333 to 0.0000 without increasing benign refusal rate. Output filtering alone produced only a small ASR reduction, from 0.3333 to 0.3000. These results should be interpreted cautiously because attack success is labeled by transparent heuristics rather than by a human or external judge, and the input guard was designed around the benchmark's known attack categories.

## Experiment Log
- Project converted from three-person plan to single-person execution.
- Obsolete role-specific planning docs removed.
- `docs/PROJECT_PLAN.md` rewritten around fixed single-person scope.
- `docs/PROJECT_STATUS.md` added as the handoff and progress tracker.
- Local model endpoint smoke test completed successfully.
- Initial thinking-output truncation was traced to too-small `max_tokens`; local config increased to 1000 tokens for official runs.
- `data/benign.csv` completed with 20 benign prompts and passed a basic CSV quality check.
- `data/attacks.csv` completed with 60 attack prompts, split evenly across `role_play`, `instruction_override`, and `obfuscation`.
- `src/run_experiment.py` implemented and verified with a two-record non-official benign run under the `none` setting.
- Code style pass completed: `src/call_model.py` and `src/run_experiment.py` were simplified, redundant defensive structure was removed, and comments were added around the main experiment flow.
- `defenses/input_guard.py` and `defenses/output_guard.py` enhanced. Static guard check: input guard blocked 60/60 attack prompts and 0/20 benign prompts. A two-record non-official input-guard run confirmed blocked records are written correctly.
- `src/evaluate_results.py` implemented and verified on the current four-record non-official raw sample. It writes `summary_by_defense.csv`, `asr_by_category.csv`, and `latency_by_defense.csv`.
- Full 320-record official experiment matrix completed with 0 runtime/API errors.
- Final summary CSVs generated under `results/summary/` and key metrics copied into this report.
