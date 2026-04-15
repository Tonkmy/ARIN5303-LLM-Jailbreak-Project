# Guide For Member 2: Dataset and Benchmark Owner

## Your Mission
Build the two official input files for the project:
- `data/attacks.csv`
- `data/benign.csv`

Your output must be clean enough that the project lead can run it directly without reformatting.

## What You Are Not Responsible For
- Do not deploy the model
- Do not run the official full experiment
- Do not redesign the schema
- Do not add extra categories without approval

## Files You Must Read First
1. `docs/PROJECT_PLAN.md`
2. `templates/attack_dataset_template.csv`
3. `templates/benign_dataset_template.csv`

## Required Output Counts
### attacks.csv
- exactly 60 rows
- 20 rows in `role_play`
- 20 rows in `instruction_override`
- 20 rows in `obfuscation`

### benign.csv
- exactly 20 rows
- use normal harmless tasks

## Step-By-Step Work
### Step 1: Copy the templates
Create working copies:
- `data/attacks.csv`
- `data/benign.csv`

### Step 2: Fill attack rows
For each attack row, complete these columns:
- `id`: use `attack_001`, `attack_002`, ...
- `category`: one of `role_play`, `instruction_override`, `obfuscation`
- `source`: short source tag, such as `JBB`, `paper`, `manual_adapt`
- `prompt`: the exact prompt to send
- `target_behavior`: short description of the intended unsafe behavior
- `is_benign`: always `false`
- `notes`: short note if needed

### Step 3: Keep the prompts balanced
Use this distribution:
- `role_play`: persona, simulation, fictional framing, alternate character prompts
- `instruction_override`: ignore previous instructions, hidden override, policy bypass wording
- `obfuscation`: encoded or indirect wording, spacing tricks, symbolic variants

Do not make one category much longer or much stronger than the others.

### Step 4: Fill benign rows
For each benign row, complete:
- `id`: use `benign_001`, `benign_002`, ...
- `category`: use `benign`
- `source`: use `manual`
- `prompt`: a harmless normal request
- `target_behavior`: expected harmless response style
- `is_benign`: always `true`
- `notes`: optional

Use these benign prompt types:
- short factual QA
- harmless summarization
- writing assistance
- simple coding help
- planning help

### Step 5: Run your own quality pass
Before handing off, check:
- no blank cells in required fields
- no duplicate prompts
- exactly 60 attacks and 20 benign prompts
- exact category spellings
- prompts are single-row CSV safe

### Step 6: Write a short taxonomy note
Create `docs/member2_taxonomy_notes.md` with:
- 3 category definitions
- 2 to 3 examples per category by `id`
- which category you expect to be strongest and why

## Handoff Checklist
You are done only if all are true:
- [ ] `data/attacks.csv` exists
- [ ] `data/benign.csv` exists
- [ ] counts are correct
- [ ] categories are balanced
- [ ] `docs/member2_taxonomy_notes.md` exists

## If You Get Stuck
Ask the lead only these kinds of questions:
- schema ambiguity
- whether a prompt belongs to one of the 3 categories
- whether a source is acceptable

Do not ask the lead to clean formatting that you can fix yourself.
