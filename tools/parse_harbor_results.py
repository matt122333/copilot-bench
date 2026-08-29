#!/usr/bin/env python3
"""Harbor job output -> results.csv (the CSV that ingest.py and report/generate.py consume).

Scans a Harbor run's jobs-dir (`harbor run ... --jobs-dir <dir>`) and, per trial, extracts
   task_id, model, run_idx, pass, elapsed_s, ttft_s, input_tokens, output_tokens,
   tokens_per_second
from:
  1) the Copilot CLI trajectory JSONL (`copilot-cli.jsonl`) that Harbor's copilot-cli agent
     writes — schema = stream events with `timestamp`, `model`, and `usage` fields.
  2) the verifier result (pass/fail) from trial/verifier JSON if present.

> Validation note: the copilot-cli.jsonl event schema is stable (timestamp/model/usage), but
> the *verifier/grade* artifact's exact path/keys vary by Harbor version. Run it once against a
> real jobs-dir and adjust `GRADE_SOURCES`/`find_grade` if the pass column comes out blank.

Usage:
  python3 tools/parse_harbor_results.py <jobs-dir> [-o runs/results.csv]
"""
from __future__ import annotations
import argparse, csv, glob, json, os, statistics

# try multiple plausible pass/fail artifacts per trial
GRADE_PATTERNS = ["*result.json", "*test.json", "*.results.json", "result*.json"]


def find_grade_json(trial_dir):
    for pat in GRADE_PATTERNS:
        hits = glob.glob(os.path.join(trial_dir, pat)) + \
               glob.glob(os.path.join(trial_dir, "**", pat), recursive=True)
        if hits:
            return hits[0]
    return None


def parse_grade(path):
    try:
        d = json.load(open(path))
    except (OSError, json.JSONDecodeError):
        return None
    for key in ("passed", "pass", "success", "passed_count", "resolved", "is_correct",
                "grade", "score"):
        v = d.get(key)
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v >= 0.5 if key in ("score", "grade") else bool(v)
    return None


def parse_trajectory(path):
    """Sum tokens, span timestamps, model name from a copilot-cli.jsonl trajectory."""
    ts, model, tin, tout, first_content = [], None, 0, 0, None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("timestamp")
        if isinstance(t, (int, float)):
            ts.append(t)
        usage = ev.get("usage") or {}
        tin += int(usage.get("input_tokens") or usage.get("input") or 0)
        tout += int(usage.get("output_tokens") or usage.get("output") or 0)
        if not model and ev.get("model"):
            model = ev["model"]
        # first non-system, non-error event with content = first response (approx TTFT)
        etype = ev.get("type")
        if (etype in ("message", "assistant", "content", "tool_use")
                or ev.get("role") == "assistant"):
            if first_content is None:
                first_content = t
    if not ts:
        return None
    elapsed = max(ts) - min(ts)
    ttft = (first_content - min(ts)) if first_content is not None else None
    toks = tin + tout
    return {
        "elapsed_s": round(elapsed, 3),
        "ttft_s": round(ttft, 3) if ttft is not None else None,
        "input_tokens": tin, "output_tokens": tout,
        "model": model or "",
        "tokens_per_second": round(toks / elapsed, 2) if elapsed > 0 else None,
    }


def walk_jobs_dir(root):
    rows = []
    for dirpath, dirnames, files in os.walk(root):
        # skip verifier docker mounts/artifacts dirs that aren't trial output
        if any(seg in dirpath.split(os.sep) for seg in ("artifacts", ".git", "verifier-copy")):
            continue
        for f in files:
            if f == "copilot-cli.jsonl":
                tp = os.path.join(dirpath, f)
                traj = parse_trajectory(tp)
                if traj is None:
                    continue
                grade = parse_grade(find_grade_json(dirpath))
                # task/model best-effort from dir naming
                parts = [p for p in dirpath.split(os.sep) if p]
                task_id = next((p for p in reversed(parts) if p not in (
                    "trials", "job", "runs", "results", "agent", "env", os.pardir)), "")
                row = {"task_id": task_id, "batch": "", "category": "", "format": "",
                       "model": traj.pop("model"), "run_idx": "1", "pass": grade,
                       "prompt_preview": "", **traj}
                m = __import__("re").search(r"/B(\d+)/", dirpath)
                if m:
                    bnum = int(m.group(1))
                    cat = {1: "coding_accuracy", 2: "agentic_terminal",
                           3: "agentic_terminal", 4: "security",
                           5: "modernization_refactor"}.get(bnum, "")
                    fmt = "single_shot" if task_id.startswith(("CSQ-", "python-")) else "agentic_terminal"
                    row.update(batch=f"B{bnum}", category=cat, format=fmt)
                rows.append(row)
                break  # one trajectory per trial dir
    return rows


def dedupe_squash_cross_task(root, rows):
    # no-op unless we later add per-task dir resolution; keeps rows as-is.
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs_dir", help="Harbor --jobs-dir output")
    ap.add_argument("-o", "--out", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                        "runs", "results.csv"))
    args = ap.parse_args()
    if not os.path.isdir(args.jobs_dir):
        raise SystemExit(f"not a dir: {args.jobs_dir}")
    rows = walk_jobs_dir(args.jobs_dir)
    if not rows:
        print(f"[warn] no copilot-cli.jsonl trajectories found under {args.jobs_dir}")
        return 1
    cols = ["task_id", "batch", "category", "format", "model", "run_idx", "pass",
            "elapsed_s", "ttft_s", "input_tokens", "output_tokens", "tokens_per_second",
            "prompt_preview"]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} runs -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())