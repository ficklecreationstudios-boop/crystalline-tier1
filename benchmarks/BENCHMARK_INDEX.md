# Crystalline Tier 1 — Benchmark Archive Index

**Status:** Historical / quarantined during founder-audit remediation  
**Original artifact date:** March 24, 2026

This directory contains benchmark scripts and outputs produced before the founder-audit remediation. The artifacts are retained for provenance, but their measurements are **not** current performance evidence and do not support blanket speed, competitiveness, production-readiness, or GPU claims.

## Archive contents

- `BENCHMARK_SUMMARY.md` — evidence-bounded historical summary.
- `BENCHMARK_REPORT.md` — preserved historical timing tables with limitations.
- `benchmark_results.json` — raw historical result data.
- `benchmark_report.html` — historical dashboard replaced by an audit notice.
- `advanced_baseline_comparison.py` — historical comparison harness.
- `advanced_benchmark.py` — historical benchmark harness.
- `comprehensive_benchmark.py` — historical benchmark harness.
- `quick_benchmark.py` — historical quick benchmark.
- `report_generator.py` — historical report generator.

## Why the original conclusions were quarantined

The audit found multiple benchmark generations and environments mixed together. Some reports also compared different numerical paths or made conclusions broader than the measurements justified. In particular, the archive does not establish:

- a universal speed-up factor;
- a claim that Crystalline is within a fixed percentage of specialized libraries;
- production suitability based on timing tables alone;
- GPU execution in Tier 1; or
- future-tier speed-up forecasts such as 10–100x or 100–3000x.

Individual historical timings may be useful as provenance, but they should not be presented as current capability measurements.

## Replacement benchmark gate

A new performance benchmark is intentionally **not** being claimed by this remediation yet. It should be generated only after numerical correctness is independently validated and should pin:

1. exact git commit and working-tree state;
2. Python, NumPy, SciPy, and benchmark-script versions;
3. CPU, OS, BLAS/LAPACK, and thread configuration;
4. identical mathematical semantics across implementations;
5. warm-up and repetition policy;
6. raw timing observations and statistical summaries; and
7. cold-start versus steady-state behavior.

The repository's current public position is therefore simple: **Tier 1 is a CPU-only NumPy/SciPy numerical utility library; performance claims remain operation- and environment-specific until a reproducible replacement benchmark is produced.**
