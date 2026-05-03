# ARIN5303 LLM Jailbreak Project

Single-operator workspace for a compact LLM jailbreak evaluation.

Start here:
1. Read `docs/PROJECT_STATUS.md` for current progress and next actions.
2. Read `docs/PROJECT_PLAN.md` for the fixed scope and execution plan.
3. Maintain `report.md` as the working final-report draft.

Core rule:
- All official experiment runs must use the same local omlx Qwen 35B 8bit MoE endpoint, system prompt, prompt template, and decoding config.

Main target:
- Run 3 jailbreak attack categories against the local model, compare no defense, input guard, output guard, and layered defense, then report ASR, benign refusal rate, and latency.
