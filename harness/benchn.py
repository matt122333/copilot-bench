#!/usr/bin/env python3
"""Copilot-Bench interactive runner.

Pick a batch (1-5) or a custom task subset -> pick model(s) -> reasoning effort
-> run through Harbor with the Copilot CLI agent, tracing telemetry to Langfuse.

Usage:
  python3 harness/benchn.py
  python3 harness/benchn.py --batch 4 --model grok-4.6 --effort medium
"""
from __future__ import annotations
import argparse, os, subprocess, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "batches"))

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

SPEC = os.path.join(ROOT, "batches", "spec.yaml")
HARBOR_ARGS = ["harbor", "run"]


def load_spec():
    return yaml.safe_load(open(SPEC))


def pick(question, options, default_idx=0):
    print(f"\n{question}")
    for i, o in enumerate(options, 1):
        mark = " (default)" if i == default_idx + 1 else ""
        print(f"  {i}) {o}{mark}")
    while True:
        r = input("> ").strip()
        if not r:
            return options[default_idx]
        if r.isdigit() and 1 <= int(r) <= len(options):
            return options[int(r) - 1]
        print("  invalid, try again.")


def multi_pick(question, options):
    print(f"\n{question} (comma-separated numbers, or 'all')")
    for i, o in enumerate(options, 1):
        print(f"  {i}) {o}")
    r = input("> ").strip().lower()
    if r == "all":
        return options
    idx = [int(x) - 1 for x in r.split(",") if x.strip().isdigit()]
    return [options[i] for i in idx if 0 <= i < len(options)]


def model_slugs(spec):
    m = spec["meta"]["models"]
    return [f"{x['id']}   ({x['label']})" + ("  [BASELINE]" if x.get("kind") == "baseline" else "") for x in m]


def resolve_model(spec, display):
    for x in spec["meta"]["models"]:
        if display.startswith(x["id"]):
            return x["id"]
    return display.split()[0]


def run(batch_id, models, effort, nconcurrent, extra_args, custom_dir=None, jobs_dir=None):
    # 1) materialize the batch dataset
    if not custom_dir:
        print(f"\n[build] materializing B{batch_id} ...")
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_datasets.py"),
                        str(batch_id)], cwd=ROOT, check=True)
        ds = os.path.join(ROOT, "batches", f"B{batch_id}")
    else:
        ds = custom_dir

    print(f"[run] dataset: {ds}  | effort={effort}  | n-concurrent={nconcurrent}")
    for model in models:
        # reasoning effort is a Harbor agent kwarg, not a generic --effort flag:
        cmd = HARBOR_ARGS + ["-d", ds, "-a", "copilot-cli", "-m", model,
                             "--ak", f"reasoning_effort={effort}",
                             "--n-concurrent", str(nconcurrent)]
        if jobs_dir:
            cmd += ["--jobs-dir", jobs_dir]
        if extra_args:
            cmd += extra_args.split()
        joined = " ".join(cmd)
        print(f"\n>>> {joined}")
        # run in foreground; long jobs should be launched with --background by the operator
        subprocess.run(cmd, cwd=ROOT, check=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", type=int, help="batch id 1-5")
    ap.add_argument("--model", action="append", help="model id (repeatable, default: all)")
    ap.add_argument("--effort", default=None, choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--n-concurrent", type=int, default=8)
    ap.add_argument("--custom-dir", help="path to a custom dataset dir (skip batch build)")
    ap.add_argument("--jobs-dir", default=None,
                    help="directory Harbor writes job results to (feed to parse_harbor_results.py)")
    ap.add_argument("--extra", default="", help="extra args passed to harbor run")
    args = ap.parse_args()

    spec = load_spec()
    batches = spec["batches"]

    # --- batch selection ---
    batch_id = args.batch
    if batch_id is None:
        print("\n=== Copilot-Bench : batch selection ===")
        for b in batches:
            print(f"\n  B{b['id']} — {b['name']}")
            print(textwrap.fill("   covers: " + b["coverage"].replace("\n", " "), 96, initial_indent="   ", subsequent_indent="   "))
        choice = input("\nPick batch (1-5), or 'custom': ").strip()
        if choice.lower() in ("custom", "c"):
            cdir = input("Custom dataset/task dir path: ").strip()
            batch_id = None; args.custom_dir = cdir
        else:
            batch_id = int(choice)

    # --- model selection ---
    slugs = model_slugs(spec)
    models = args.model or multi_pick("\nSelect model(s)", slugs)
    models = [resolve_model(spec, m) for m in models]

    # --- reasoning effort ---
    effort = args.effort or pick("\nReasoning effort (identical for all models to stay controlled)",
                                 ["low", "medium", "high", "xhigh", "max"], default_idx=1)

    nconc = args.n_concurrent

    run(batch_id, models, effort, nconc, args.extra,
        custom_dir=args.custom_dir, jobs_dir=args.jobs_dir)


if __name__ == "__main__":
    main()