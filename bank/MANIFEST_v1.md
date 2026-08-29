# Copilot-Bench — Task Governance Manifest (v1)

- **Status:** FROZEN on approval (see sign-off) — the locked task set for all runs
- **Harness:** GitHub Copilot CLI (via Harbor), `copilot-cli` agent
- **Models:** grok-4.6 · opus-5 · msai-flash · gemini-3.7-flash | **baseline:** opus-4.8
- **Config (controlled):** reasoning effort = medium, 1 pass, web=off, MCP=none,
  per-task timeouts, all tools on. **Only `--model` varies.**

## Governance rules
1. The runner consumes **only** tasks listed here — no ad-hoc prompts at runtime.
2. **Provenance:** `custom` = private/novel (contamination control, never published);
   stock entries = pinned **public** Harbor datasets, graded by their published verifiers.
3. **Deterministic grading:** Harbor oracle + verifier in a separate container; hashed
   answers; `environment_mode=separate`.
4. Source of truth: `batches/spec.yaml`. Changes require a manifest bump + re-approval.

## Task set (43)

### B1 · Single-shot coding accuracy — 12 (custom)
`custom_tasks/CSQ-01_get_norm, CSQ-02_valid_braces, CSQ-03_deep_merge, CSQ-04_to_snake_case,
CSQ-05_str_compress, CSQ-06_is_palindrome_perm, CSQ-07_top_k_frequent, CSQ-08_matrix_rotate,
CSQ-09_semver_compare, CSQ-10_is_anagram, CSQ-11_find_dupes, CSQ-12_lru_cache`

### B2 · Agentic terminal A (software/data) — 8 (terminal-bench@latest)
mvcc-lsm-compaction · payments-pipeline-fix · live-database-cutover · react-lead-form ·
session-window-debug · cumulative-layout-shift · legacy-utility-triage · production-planning

### B3 · Agentic terminal B (ML/data-eng) — 7 (terminal-bench@latest)
data-anonymization · distributed-dedup · vllm-deepseek-streaming · sglang-qwen-burst ·
embedding-drift-monitor · batched-eval-parity · mp-checkpoint-consolidation

### B4 · Security — 8 (terminal-bench@latest + binary-audit@1.0)
shadow-relay · uefi-bootkit · formal-crypto · interleaved-vigenere · html-js-filter ·
( binary-audit ) caddy-backdoor-detect · dnsmasq-backdoor-detect · lighttpd-backdoor-detect

### B5 · Modernization / refactoring — 8 (crustbench@1.0 + terminal-bench@latest)
( crustbench ) crustbench-2dpartint · crustbench-amp · crustbench-approxidate · crustbench-bigint ·
crustbench-bitset · crustbench-btree-map · ( terminal-bench ) vba-userform-port · vf2-speedup-networkx

## Metrics
task-success (pass%) · TTFT · tokens/sec · throughput · cost/task (needs price sheet) ·
latency · variability (requires run_idx≥2). All logged to Langfuse + report.

## Sign-off (pre-approval for regulated use)
- [ ] Task set approved (owner): ______________  date: ______
- [ ] Models/versions frozen: ______________
- [ ] Reasoning effort locked (medium): ______________
- [ ] Price sheet filled (cost/task): ⬜ not required for pass-only audit