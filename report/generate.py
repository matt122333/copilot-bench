#!/usr/bin/env python3
"""Aggregate Copilot-Bench results into an audit report (markdown).

Input: results CSV (same schema as langfuse/ingest.py) OR a dir of CSVs.
Output: reports/report_<ts>.md — per-batch & per-category × model tables:
  pass rate, cost/task, latency, TTFT, tokens/sec, variance (when run_idx>1).

Usage:
  python3 report/generate.py runs/batch1_results.csv [runs/batch2_results.csv ...]
"""
from __future__ import annotations
import csv, collections, os, sys, statistics, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")


def load_rows(paths):
    rows = []
    for p in paths:
        try:
            rows += list(csv.DictReader(open(p)))
        except OSError as e:
            print("skip", p, e)
    return rows


def num(r, k):
    try:
        return float(r.get(k))
    except (TypeError, ValueError):
        return None


def fmt(x):
    if x is None:
        return "N/A"
    return f"{x:.3f}" if isinstance(x, float) else str(x)


def agg(rows):
    """Group by (batch,category) then model -> metric table."""
    out = collections.OrderedDict()
    for r in rows:
        key = (r.get("batch"), r.get("category"))
        out.setdefault(key, collections.OrderedDict())
        out[key].setdefault(r["model"], []).append(r)
    return out


def stats_for(mod_runs):
    n = len(mod_runs)
    passr = sum(1 for r in mod_runs if str(r.get("pass")).lower() in ("1", "true", "yes", "pass")) / n
    el = [num(r, "elapsed_s") for r in mod_runs]
    tt = [num(r, "ttft_s") for r in mod_runs]
    toks = [num(r, "tokens_per_second") for r in mod_runs if num(r, "tokens_per_second") is not None]
    cost = [num(r, "cost") for r in mod_runs if num(r, "cost") is not None]

    def agg2(xs):
        xs = [x for x in xs if x is not None]
        if not xs:
            return None, None, None
        m = statistics.mean(xs)
        s = statistics.stdev(xs) if len(xs) > 1 else None
        return m, s, len(xs)

    mean_el, sd_el, _ = agg2(el)
    mean_tt, _, _ = agg2(tt) if False else (statistics.mean([t for t in tt if t is not None]) if [t for t in tt if t is not None] else None, None, None)
    mean_tok, sd_tok, _ = agg2(toks)
    mean_cost, sd_cost, _ = agg2(cost)
    return {
        "n": n, "pass_rate": passr, "elapsed": mean_el, "elapsed_sd": sd_el,
        "ttft": mean_tt, "tps": mean_tok, "tps_sd": sd_tok,
        "cost": mean_cost, "cost_sd": sd_cost,
    }


def render(rows):
    grp = agg(rows)
    L = []
    L.append("# Copilot-Bench — Audit Report")
    L.append(f"_generated {datetime.datetime.now().isoformat(timespec='seconds')}_\n")
    for (batch, cat), models in grp.items():
        L.append(f"\n## Batch {batch} · {cat or ''}")
        L.append("| model | n | pass% | elapsed(s)±σ | TTFT(s) | tok/s±σ | cost/task±σ |")
        L.append("|---|---|---|---|---|---|---|")
        for model, runs in models.items():
            s = stats_for(runs)
            L.append(f"| {model} | {s['n']} | {s['pass_rate']*100:.1f}% | "
                     f"{fmt(s['elapsed'])}{'±'+fmt(s['elapsed_sd']) if s['elapsed_sd'] else ''} | "
                     f"{fmt(s['ttft'])} | {fmt(s['tps'])}{'±'+fmt(s['tps_sd']) if s['tps_sd'] else ''} | "
                     f"{fmt(s['cost'])}{'±'+fmt(s['cost_sd']) if s['cost_sd'] else ''} |")
    L.append("\n_note: single-pass cells have no σ (variance needs run_idx≥2). "
             "Costs are N/A until price_sheets/models.yaml is filled._\n")
    return "\n".join(L)


def main():
    paths = sys.argv[1:]
    if not paths:
        sys.exit("usage: report/generate.py <results.csv> [...]")
    rows = load_rows(paths)
    md = render(rows)
    os.makedirs(REPORTS, exist_ok=True)
    fn = os.path.join(REPORTS, f"report_{datetime.datetime.now():%Y%m%d_%H%M%S}.md")
    open(fn, "w").write(md)
    print(f"wrote {fn} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())