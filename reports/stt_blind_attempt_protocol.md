# STT Blind Attempt Protocol

Date: 2026-05-15

Purpose: obtain clean-room theorem attempts before exposing a model to the STT
frontier notes or literature context.

## Prompt

Use exactly:

- `reports/stt_true_blind_prompt.md`

Do not include repository files, source summaries, known examples, author
names, or internet access in the blind attempt thread.

## Runs

Run two fresh threads:

1. GPT-5 primary blind attempt.
   - Use the highest reasoning level available.
   - Allow a sustained serious session.
   - Do not browse.
   - Do not attach repository context.

2. Claude Opus 4.7 extended-thinking cross-check.
   - Use one focused deep pass.
   - Avoid multi-turn coaching or iterative hints.
   - Do not browse.
   - Do not attach repository context.

Codex should not run these blind attempts. Codex only maintains this protocol
and the prompt files.

## Output Files

Save outputs verbatim as:

- `reports/stt_blind_attempt_001_gpt5.md`
- `reports/stt_blind_attempt_001_claude_opus_4_7.md`

Each output file must begin with this metadata header:

```text
---
model_name: TODO
reasoning_setting: TODO
date: TODO
clean_room_attestation: "No internet, no repository context, no literature notes, and no prior STT frontier context were used."
---
```

After the metadata header, paste the model output without editing except for
obvious transcript formatting needed to preserve readability.
