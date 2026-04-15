# Task Board

## Member 1: Lead / Experiment Owner
### Week 1
- [ ] Confirm local `curl` endpoint, model name, and stable parameters
- [ ] Fill `configs/model_api.json`
- [ ] Freeze system prompt and output schema
- [ ] Run smoke test on 10 prompts

### Week 2
- [ ] Integrate `data/attacks.csv` and `data/benign.csv`
- [ ] Integrate both defenses
- [ ] Run `none`, `input_guard`, `output_guard`, and `input_guard+output_guard`
- [ ] Save outputs under `results/`

### Week 3
- [ ] Review failed cases
- [ ] Rerun final matrix if needed
- [ ] Hand clean results to Member 3
- [ ] Final QC before submission

## Member 2: Dataset Owner
### Week 1
- [ ] Finish `data/attacks.csv`
- [ ] Finish `data/benign.csv`
- [ ] Keep exactly 20 attack prompts per category
- [ ] Record sources in `source`
- [ ] Review prompt wording for consistency

### Week 2
- [ ] Audit strange or broken prompts after smoke test
- [ ] Fix duplicates and category mistakes
- [ ] Write short taxonomy summary for report

### Week 3
- [ ] Select representative cases for presentation
- [ ] Help verify whether attack labels match observed outputs

## Member 3: Defense / Evaluation / Report Owner
### Week 1
- [ ] Implement defense stubs
- [ ] Implement evaluation skeleton
- [ ] Define refusal and success logic

### Week 2
- [ ] Refine input guard
- [ ] Refine output guard
- [ ] Produce first summary table

### Week 3
- [ ] Produce 3 final charts
- [ ] Draft report
- [ ] Draft slides
- [ ] Prepare speaking notes
