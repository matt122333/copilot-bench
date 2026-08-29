# Custom tasks (contamination-control / single-shot track)

This directory holds **12 bespoke single-shot coding-accuracy tasks** (CSQ-01…12).
These are our own, **never published**, so models cannot have memorized them — they
serve double duty:

1. **Single-shot track** — the flash-friendly modality (one prompt → one answer)
   that Harbor's public datasets don't cover well.
2. **Contamination control** — comparing each model's public-vs-private pass rate
   exposes whether it has memorized public benchmarks.

The agentic / security / modernization categories are intentionally **stock
(out-of-the-box)** — see `batches/spec.yaml` → terminal-bench, binary-audit, crustbench.

## Task anatomy (Harbor format)

Each `CSQ-XX_*/` directory:
```
task.toml            metadata + verifier/agent timeouts + env (environment_mode=separate)
instruction.md       the EXACT prompt the model receives (spec + hidden reference tests)
environment/solution.py  stub the model edits at /workspace/solution.py
solution/solution.py     oracle — proves the task is solvable (verified)
tests/test_csqXX.py      deterministic grader: loads /workspace/solution.py and asserts
```

**Verification:** every oracle passes its own grader (`tools/build_custom_tasks.py`
verifies all 12). Graders are pure-Python hidden assertions — no external tooling.

## Regenerate

```bash
python3 tools/build_custom_tasks.py     # rebuilds CSQ-02..12; CSQ-01 is hand-written
```