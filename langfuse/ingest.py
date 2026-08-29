#!/usr/bin/env python3
"""Ingest benchmark results into self-hosted Langfuse for the audit trail.

Input:  a results CSV produced by the runner / a post-run parser:
        task_id, batch, category, format, model, run_idx, pass, elapsed_s,
        ttft_s, input_tokens, output_tokens, reasoning_tokens
Output: one Langfuse trace + generation per (task × model × run), tagged for
        audit queries (batch/category/model-kind). Cost computed from price sheet.

Usage:
  LANGKFUSE_PK=... LANGKFUSE_SK=... LANGKFUSE_HOST=http://localhost:3000 \
      python3 langfuse/ingest.py runs/batch1_results.csv

Requires: pip install langfuse pyyaml
Placeholders below read credentials from env (never commit secrets).
"""
from __future__ import annotations
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def load_price_sheet():
    import yaml
    p = os.path.join(ROOT, "price_sheets", "models.yaml")
    return yaml.safe_load(open(p))["models"]


def cost_for(price, model, in_tok, out_tok):
    m = price[model]
    if not m["price_in_per_1m"] or not m["price_out_per_1m"]:
        return None
    return (in_tok / 1_000_000) * m["price_in_per_1m"] + \
           (out_tok / 1_000_000) * m["price_out_per_1m"]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    results_file = sys.argv[1]
    pk = os.environ.get("LANGKFUSE_PK") or os.environ.get("LANGFUSE_PUBLIC_KEY")
    sk = os.environ.get("LANGKFUSE_SK") or os.environ.get("LANGFUSE_SECRET_KEY")
    host = os.environ.get("LANGKFUSE_HOST", "http://localhost:3000")
    if not (pk and sk):
        print("[skip] LANGKFUSE_PK/LANGKFUSE_SK not set — no telemetry sent.", file=sys.stderr)
        return 0

    from langfuse import Langfuse
    lf = Langfuse(public_key=pk, secret_key=sk, host=host)
    price = load_price_sheet()

    rows = list(csv.DictReader(open(results_file)))
    print(f"ingesting {len(rows)} runs into Langfuse@{host}")
    for r in rows:
        model = r["model"]
        in_tok = int(r.get("input_tokens") or 0)
        out_tok = int(r.get("output_tokens") or 0)
        elapsed = float(r.get("elapsed_s") or 0)
        ttft = float(r.get("ttft_s") or 0)
        tok_s = (in_tok + out_tok) / elapsed if elapsed else None
        cost = cost_for(price, model, in_tok, out_tok)
        usage = {"input": in_tok, "output": out_tok, "unit": "TOKENS"}
        trace = lf.trace(
            name=f"B{r['batch']}/{r['task_id']}",
            input={"prompt": r.get("prompt_preview", "")},
            output={"pass": r.get("pass")},
            metadata={
                "task_id": r["task_id"], "batch": r["batch"],
                "category": r.get("category", ""), "format": r.get("format", ""),
                "model": model, "run_idx": r.get("run_idx"),
                "ttft_s": ttft, "elapsed_s": elapsed,
                "tokens_per_second": tok_s,
                "cost": cost,
            },
        )
        trace.generation(
            name="copilot-cli.run",
            model=model,
            model_parameters={"reasoning_effort": r.get("effort", "medium")},
            usage=usage,
            cost=cost,
            start_time=None,
            metadata={"batch": r["batch"], "task_id": r["task_id"],
                      "pass": r.get("pass")},
        )
        trace.update()
    lf.flush()
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())