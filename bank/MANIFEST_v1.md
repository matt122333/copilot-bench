# Copilot-Bench — Task Governance Manifest (v1)

- **Status:** FROZEN on approval (see sign-off) — the locked task set for all runs
- **Harness:** GitHub Copilot CLI (via Harbor), `copilot-cli` agent
- **Models:** grok-4.6 · opus-5 · msai-flash · gemini-3.7-flash | **baseline:** opus-4.8
- **Config (controlled):** reasoning effort = medium, 1 pass, web=off, MCP=none,
  per-task timeouts, all tools on. **Only `--model` varies.**

## Composition (50 = 25 custom + 25 stock)
- **25 custom** (`custom_tasks/`): private/novel — the contamination-control set + the
  single-shot / agentic / security / modernization coverage that public sets lack.
- **25 stock** (public, pinned Harbor datasets): terminal-bench@latest, binary-audit@1.0,
  crustbench@1.0, humanevalfix@1.0 — graded by their published verifiers.

## Governance rules
1. The runner consumes **only** tasks listed here — no ad-hoc prompts at runtime.
2. Every task carries **provenance**: `custom` (private, never published) or a pinned **public** dataset.
3. **Deterministic grading:** Harbor oracle + verifier in a separate container; hashed answers;
   `environment_mode=separate`. Private tasks verified oracle-green before commit.
4. Source of truth: `batches/spec.yaml`. Changes require a manifest bump + re-approval.

## Task set (50) — see batches/spec.yaml for IDs

| Batch | Category | custom | stock | total |
|---|---|---|---|---|
| B1 | Single-shot coding accuracy | 12 (CSQ-01..12) | 3 (humanevalfix) | 15 |
| B2 | Agentic terminal A (software/data) | 2 (CAT-01..02) | 5 (terminal-bench) | 7 |
| B3 | Agentic terminal B (ML/data-eng) | 1 (CAT-03) | 4 (terminal-bench) | 5 |
| B4 | Security | 4 (CSE-01..04) | 5 (TB + binary-audit) | 9 |
| B5 | Modernization / refactoring | 6 (CMO-01..06) | 8 (crustbench + TB) | 14 |
| **total** | | **25** | **25** | **50** |

Private task detail: CSQ-01..12 single-shot (get_norm, valid_braces, deep_merge, to_snake_case,
str_compress, is_palindrome_perm, top_k_frequent, matrix_rotate, semver_compare, is_anagram,
find_dupes, lru_cache) · CAT-01..03 agentic (rename-symbol, fix-import, reduce-noise) ·
CSE-01..04 security (path-traversal, SQLi, JWT, TLS-harden) · CMO-01..06 modernization
(py2-to-py3, argparse→subparsers, sync→asyncio, Makefile→just, React class→hooks, C→Rust).

## Metrics
task-success (pass%) · TTFT · tokens/sec · throughput · cost/task (needs price sheet) ·
latency · variability (requires run_idx≥2). All logged to Langfuse + report.

## Sign-off (pre-approval for regulated use)
- [ ] Task set approved (owner): ______________  date: ______
- [ ] Models/versions frozen: ______________
- [ ] Reasoning effort locked (medium): ______________
- [ ] Price sheet filled (cost/task): ⬜ not required for pass-only audit