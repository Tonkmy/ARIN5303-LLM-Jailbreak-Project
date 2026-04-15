# Project Plan

## One-Sentence Scope
Evaluate 3 jailbreak attack categories against a locally served Qwen 35B 8bit model, then compare no defense, input defense, output defense, and layered defense on ASR and benign refusal rate.

## Why This Scope
This is the smallest version that still looks like a real security evaluation project.
It is realistic for 3 people and 3 weeks.

## Fixed Decisions
- Main model: local Qwen 35B 8bit API
- Official attack categories: `role_play`, `instruction_override`, `obfuscation`
- Official defenses:
  - input guard
  - output guard
- Official experiment settings:
  - same system prompt
  - same temperature
  - same max tokens
  - same model endpoint

## Deliverables
1. Clean benchmark files
   - `data/attacks.csv`
   - `data/benign.csv`
2. Runnable experiment pipeline
   - `src/call_model.py`
   - `src/run_experiment.py`
3. Two defense modules
   - `defenses/input_guard.py`
   - `defenses/output_guard.py`
4. Evaluation outputs
   - summary table
   - 3 charts
5. Final report and slides

## Roles
### Lead / Member 1
Owns:
- local model endpoint
- integration
- official runs
- final results
- keeping schedule tight

### Member 2
Owns:
- attack set
- benign set
- dataset quality checks
- source tracking

### Member 3
Owns:
- defense implementations
- evaluation script
- figures
- report draft

## Dataset Target
### Attack set
- 60 total attack prompts
- 20 per category
- use public benchmark ideas and known jailbreak styles
- do not create extra scope by collecting too many sources

### Benign set
- 20 total benign prompts
- a mix of normal QA, summarization, coding help, and harmless advice

## Experiment Matrix
Run these 4 settings only:
1. `none`
2. `input_guard`
3. `output_guard`
4. `input_guard+output_guard`

Do not add more variants unless the first 4 are complete.

## Metrics
### Primary
- ASR: fraction of attack prompts that produce a successful unsafe completion
- benign refusal rate: fraction of benign prompts incorrectly blocked or refused

### Secondary
- average latency per prompt

## Three-Week Schedule
### Week 1: Freeze Inputs
- Member 2 finishes first-pass datasets
- Lead verifies local pipeline and result schema
- Member 3 writes defense stubs and evaluation skeleton
- Team runs 5 to 10 sample prompts as smoke test

### Week 2: Run Core Experiments
- Lead runs baseline and defended experiments on the full set
- Member 3 fixes defenses based on observed failures
- Member 2 audits mislabeled prompts and cleans data

### Week 3: Finish Story
- Lead reruns the final experiment matrix if needed
- Member 3 generates charts and report draft
- Member 2 writes taxonomy and attack case analysis
- Team prepares final slides and speaking order

## Success Criteria
The project is complete if:
- all 4 experiment settings are run on the same dataset
- ASR and benign refusal rate are reported
- at least 3 clear figures or tables are produced
- the report explains which attack category is strongest and which defense helps most
