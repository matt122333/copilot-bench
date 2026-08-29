#!/usr/bin/env python3
"""Harbor job output -> results.csv (the CSV that ingest.py and report/generate.py consume).

Scans a Harbor run's jobs-dir (`harbor run ... --jobs-dir <dir>`) and, per trial, extracts
   task_id, batch, category, format, model, run_idx, pass, elapsed_s, ttft_s,
   input_tokens, output_tokens, tokens_per_second
from:
  1) the Copilot CLI trajectory JSONL (`copilot-cli.jsonl`) that Harbor's copilot-cli agent
     writes — schema = stream events with `timestamp`, `model`, and `usage` fields.
  2) the verifier result (pass/fail) from trial/verifier JSON if present.

task_id / batch / category / format are resolved from the KNOWN task list in batches/spec.yaml
(not from the leaf dir name, so trial-dir names don't corrupt the audit grouping).

For multi-pass variance: run with `--run-idx 1`, `--run-idx 2`, ... per pass (and merge the CSVs),
or repeat a batch twice per model.

Usage:
  python3 tools/parse_harbor_results.py <jobs-dir> -o runs/results.csv [--run-idx N]
"""
from __future__ import annotations
import argparse, csv, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "batches", "spec.yaml")

GRADE_PATTERNS = ["*result.json", "*test.json", "*.results.json", "result*.json"]


def load_spec_map():
    """task_id -> (batch, category, format) built from the governance spec."""
    import yaml
    spec = yaml.safe_load(open(SPEC))
    out = {}
    cat_by_id = {1: "coding_accuracy", 2: "agentic_terminal", 3: "agentic_terminal",
                 4: "security", 5: "modernization_refactor"}
    for b in spec["batches"]:
        for t in b["tasks"]:
            out[t["id"]] = ("B" + str(b["id"]), cat_by_id[b["id"]],
                            "single_shot" if t["id"].startswith(("CSQ-", "python-")) else "agentic_terminal")
    return out


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
            return bool(v) if key not in ("score", "grade", "passed_count") else v >= 0.5
    return None


def parse_trajectory(path):
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
        if (ev.get("type") in ("message", "assistant", "content", "tool_use")
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


def resolve_task(dirpath, known):
    """Find the rightmost path segment that is a known task id; return its (batch,cat,fmt)."""
    segs = [s for s in dirpath.split(os.sep) if s]
    for seg in reversed(segs):
        if seg in known:
            return seg, known[seg]
    return "", ("", "", "")


def walk_jobs_dir(root, run_idx, known):
    rows = []
    for dirpath, _, files in os.walk(root):
        if any(seg in dirpath.split(os.sep) for seg in ("artifacts", ".git", "verifier-copy")):
            continue
        if "copilot-cli.jsonl" not in files:
            continue
        traj = parse_trajectory(os.path.join(dirpath, "copilot-cli.jsonl"))
        if traj is None:
            continue
        task_id, (batch, cat, fmt) = resolve_task(dirpath, known)
        grade = parse_grade(find_grade_json(dirpath))
        rows.append({
            "task_id": task_id, "batch": batch, "category": cat, "format": fmt,
            "model": traj.pop("model"), "run_idx": str(run_idx),
            "pass": "" if grade is None else grade, "prompt_preview": "", **traj,
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs_dir", help="Harbor --jobs-dir output")
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "runs", "results.csv"))
    ap.add_argument("--run-idx", type=int, default=1,
                    help="Which pass this jobs-dir is (stamped on every row) — use 1,2,3.. for variance")
    args = ap.parse_args()
    if not os.path.isdir(args.jobs_dir):
        raise SystemExit(f"not a dir: {args.jobs_dir}")
    known = load_spec_map()
    rows = walk_jobs_dir(args.jobs_dir, args.run_idx, known)
    if not rows:
        print(f"[warn] no copilot-cli.jsonl trajectories found under {args.jobs_dir}")
        return 1
    cols = ["task_id", "batch", "category", "format", "model", "run_idx", "pass",
            "elapsed_s", "ttft_s", "input_tokens", "output_tokens", "tokens_per_second",
            "prompt_preview"]
    # merge append if the output file already exists (multi-pass accumulation)
    mode = "a" if os.path.exists(args.out) else "w"
    wrote_header = mode == "w"
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if wrote_header:
            w.writeheader()
        w.writerows(rows)
    print(f"appended {len(rows)} runs (run_idx={args.run_idx}) -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())