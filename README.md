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
uv tool install harbor[modal]              # =0.22.0+ (0.22.0 SHIPS the `copilot-cli` agent)
pip install -r requirements.txt            # pyyaml, langfuse
# install Copilot CLI; authenticate once (needs a Copilot seat)
copilot                                  # one-time device-login (grants Copilot scope)
# auth is read from GH_TOKEN / COPILOT_GITHUB_TOKEN by the copilot-cli agent

# 1) materialize a batch dataset dir (pulls stock tasks from Harbor, copies custom)
python3 tools/build_datasets.py 4
# 2) run it: interactive (pick batch 1-5, models, reasoning effort)
python3 harness/benchn.py --jobs-dir runs/job4
#    or non-interactive:
python3 harness/benchn.py --batch 4 --model opus-5 --effort medium --n-concurrent 8 \
    --jobs-dir runs/job4
# 3) parse Harbor's job output into results.csv (the audit CSV)
python3 tools/parse_harbor_results.py runs/job4 -o runs/results.csv
# 4) ingest telemetry -> Langfuse + generate the audit report
LANGFUSE_PK=… LANGFUSE_SK=… LANGKFUSE_HOST=http://localhost:3000 \
    python3 langfuse/ingest.py runs/results.csv
python3 report/generate.py runs/results.csv
```

- `harbor` ≥ **0.22.0** — required (older releases don't resolve the `copilot-cli` agent).
- **Models for the Copilot-CLI agent are Copilot model IDs** (bare slugs, e.g. `grok-4.6`),
  not `provider/model`. They must exist in your Copilot subscription — list them via
  `/models` in an interactive `copilot` session.
- **Reasoning effort** is passed as a Harbor agent kwarg (`--ak reasoning_effort=medium`);
  `benchn.py` already does this.

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
custom_tasks/              # 25 bespoke tasks (CSQ/CAT/CSE/CMO)  [private/control]
tools/build_datasets.py    # assemble a batch dir from spec (pull stock + copy custom)
tools/parse_harbor_results.py  # Harbor --jobs-dir -> results.csv (audit CSV)
harness/benchn.py          # interactive runner (batch/model/effort → harbor run)
langfuse/                  # docker-compose (self-hosted) + ingest adapter
price_sheets/models.yaml   # provider pricing for cost/task
report/generate.py         # audit report generator
bank/MANIFEST_v1.md        # governance manifest (frozen task list + sign-off)
requirements.txt           # pyyaml, langfuse (harbor installs via uv)
```

## Metrics — what's really measurable now, vs planned

Honest split:

- **Task track (produces today, via Harbour + Copilot CLI trajectory):** pass%, **token counts**
  (in/out), **elapsed time**, **tokens/sec** and an approximate **TTFT** (time-to-first-content
  from the trajectory) — assembled by `tools/parse_harbor_results.py`. **cost/task** once you fill
  `price_sheets/models.yaml`.
- **Performance track (planned/separate harness):** true TTFT, throughput at concurrency, p50/p95,
  $/token from the *raw provider API* (LiteLLM proxy + load generator → same Langfuse). Not produced
  by the Copilot-CLI task track — those columns are N/A until that harness lands.
- **Variability/consistency:** requires `run_idx` ≥ 2 (multi-pass). Default is 1 pass → pass% only,
  no error bars. Run a batch twice per model (or keep the 2-3-pass subset) to get σ/CI.

`parse_harbor_results.py` is best-effort: it targets the stable `copilot-cli.jsonl` trajectory
schema but reads the verifier pass/fail artifact heuristically — run it once against a real
jobs-dir and adjust `GRADE_PATTERNS` in that file if the pass column is blank.

*Planning/runnable scaffolding — clone it into your eval environment to run.*