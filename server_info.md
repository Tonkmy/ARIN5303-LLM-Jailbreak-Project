# Local Model Server Notes

The experiment used a local omlx server with an OpenAI-compatible chat-completions API.

## Model Check

- Endpoint checked: `/v1/models`
- Available model id: `Qwen3.5-35B-A3B-8bit`
- Provider field: `omlx`

## Smoke-Test Note

An early smoke test with a very small completion budget stopped with `finish_reason = length`. The official experiment configuration therefore uses `max_tokens = 1000`, which gives the model enough room to produce a final answer instead of stopping inside preliminary text.

The completed raw result files under `results/raw/` use the same model id and contain no runtime or API errors.
