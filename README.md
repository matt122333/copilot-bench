# Copilot-Bench

A **controlled, auditable multi-model coding benchmark** that runs the same fixed
task set through the **GitHub Copilot CLI** agent (via Harbor) across 5 models,
records full telemetry to **Langfuse**, and produces an audit report.

**Models:** Grok 4.6 · Opus 5 · MsAI Flash · Gemini 3.7 Flash  — vs **baseline Opus 4.8**
**Backend:** Harbor (docker, Modal optional) · **Harness:** `copilot-cli` agent
**Telemetry:** self-hosted Langfuse · **Metrics:** pass/task-success, TTFT, tokens/sec,
throughput, cost/task, latency, variability (multi-pass)

> Controlled experiment: **only `--model` varies.** All models get identical tools,
> web=off, MCP=none, reasoning effort, context, timeout, and the exact same fixed prompts.

---

## Quickstart

```bash
uv tool install harbor[modal]      # or:  uv tool install harbor
# install Copilot CLI; authenticate once (needs a Copilot seat)
copilot                            # one-time device-login (grants Copilot scope)
# auth is read from GH_TOKEN / COPILOT_GITHUB_TOKEN by the copilot-cli agent

# 1) materialize a batch dataset dir (pulls stock tasks from Harbor, copies custom)
python3 tools/build_datasets.py 4
# 2) run it: interactive
python3 harness/benchn.py
#    or non-interactive:
python3 harness/benchn.py --batch 4 --model opus-5 --effort medium --n-concurrent 8
# 3) ingest telemetry -> Langfuse + generate the audit report
LANGKFUSE_PK=… LANGKFUSE_SK=… LANGKFUSE_HOST=http://localhost:3000 \
    python3 langfuse/ingest.py runs/results.csv
python3 report/generate.py runs/results.csv
```

**Environment needs:** docker daemon (or Modal account), `uv`, GitHub Copilot seat.
Point Copilot CLI at your provider via `COPILOT_GITHUB_TOKEN` if you have a Copilot
API key for model routing.

---

## Batches (run in ~3h, medium effort, 1 pass)

| Batch | Coverage | Tasks |
|---|---|---|
| B1 | **Single-shot coding accuracy** — flash-friendly single-turn, hidden-test grading. ~12 novel control tasks (contamination check) **+ 3 public** humanevalfix. | 15 |
| B2 | **Agentic terminal A (software/data)** — multi-file bug hunts, DB/queue cutover, perf regressions. | 7 |
| B3 | **Agentic terminal B (ML/data-eng / cleanup)** — dedup, utility triage, output cleanup. | 5 |
| B4 | **Security** — path-traversal, SQLi, JWT, TLS hardening + binary backdoor/crypto review. Hashed determinism. | 9 |
| B5 | **Modernization / refactoring** — C→Rust, build-system ports, py2→py3, async, React hooks. | 14 |

**Total = 50 tasks = 25 custom (private, contamination-control) + 25 stock (public, out-of-box).**

```bash
python3 harness/benchn.py            # pick batch 1–5, or 'custom' dataset dir
python3 tools/build_datasets.py -l   # list batches + counts
```

---

## Governance (audit-friendly, for regulated environments)

- Tasks are **frozen + versioned** in `bank/MANIFEST_v1.md`; pre-approved before runs.
- Every task carries **provenance**: `custom` (private/novel — our contamination control)
  or a pinned **public** dataset (`terminal-bench/…@latest`, `binary-audit@1.0`, `crustbench@1.0`).
- Grading is **deterministic**: Harbor verifier + oracle; answers hashed or separate container;
  `environment_mode=separate`. Stock tasks use their published verifiers.
- All raw request/response + trajectory JSONL are captured by Harbor → retain for audit.
- Cost = tokens × `price_sheets/models.yaml` (fill in provider rates to enable cost/task).
- Single-pass = pass% only; add `run_idx` passes (min 2) to get variance/CI.

## Repo layout

```
batches/spec.yaml          # batch + model definitions, coverage text
batches/B1..B5/            # materialized datasets (generated, gitignored)
custom_tasks/                 # 25 bespoke tasks (CSQ/CAT/CSE/CMO)  [private/control]
tools/build_datasets.py    # assemble a batch dir from spec (pull stock + copy custom)
harness/benchn.py          # interactive runner (batch/model/effort → harbor run)
langfuse/                  # docker-compose (self-hosted) + ingest adapter
price_sheets/models.yaml   # provider pricing for cost/task
report/generate.py         # audit report generator
bank/MANIFEST_v1.md        # governance manifest (frozen task list + sign-off)
```

## Tracked metrics (both via Copilot + raw API)

- **Task-success track** (Copilot CLI): pass%, cost/task, latency, token efficiency, variance.
- **Performance track** (raw provider API): TTFT, tokens/sec, throughput, p50/p95, $/token —
  via LiteLLM proxy + load generator, feeding the same Langfuse. (Separate harness; see roadmap.)

*This is planning/runnable scaffolding — clone it into your eval environment to run.*