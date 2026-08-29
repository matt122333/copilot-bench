# Custom tasks (contamination-control + private category coverage)

This directory holds **25 bespoke tasks**, our own and **never published**, so models
cannot have memorized them. They serve two roles:

1. **Private category coverage** the public sets lack (esp. single-shot, plus richer
   agentic/security/modernization cases).
2. **Contamination control** — comparing each model's public-vs-private pass rate exposes
   whether it has memorized public benchmarks.

The 25 stock tasks are **out-of-the-box** public Harbor datasets — see `batches/spec.yaml`.

## Tasks (25)

- **CSQ-01..12 — single-shot coding accuracy** (hidden assert grader, pure Python):
  get_norm, valid_braces, deep_merge, to_snake_case, str_compress, is_palindrome_perm,
  top_k_frequent, matrix_rotate, semver_compare, is_anagram, find_dupes, lru_cache.
- **CAT-01..03 — agentic_terminal**: rename symbol cross-file · fix broken import ·
  quiet a noisy pipeline.
- **CSE-01..04 — security**: path-traversal · SQL injection · insecure JWT · TLS hardening.
- **CMO-01..06 — modernization**: py2→py3 · argparse→subparsers · sync→asyncio ·
  Makefile→just · React class→hooks · C→Rust mini.

## Task anatomy (Harbor format)

Each `NAME/` directory:
```
task.toml            metadata + verifier/agent timeouts + env (environment_mode=separate)
instruction.md       the EXACT prompt the model receives
environment/         seeded workdir the model edits (mounted at /workspace)
solution/            oracle — proves the task is solvable (verified oracle-green)
tests/test.sh        deterministic grader (runs from /workspace, exits 0/1)
```

## Verification
- **CSQ-01..12** + **CAT, CSE, CMO (python-gradable)** verified: every oracle passes its own
  grader (`tools/build_custom_tasks.py`, `tools/build_agentic_tasks.py`, `/tmp` smoke harness).
- Build-tool variants **CMO-04 (just), CMO-05 (node), CMO-06 (cargo)** require those toolchains
  in the eval image; graders written to Harbor convention and executed at run time.

## Regenerate
```bash
python3 tools/build_custom_tasks.py     # CSQ-02..12 (CSQ-01 hand-written); fixed graders
python3 tools/build_agentic_tasks.py    # CAT/CSE/CMO (note: generated files were further
                                        # corrected in-repo; treat committed tasks as canonical)
```