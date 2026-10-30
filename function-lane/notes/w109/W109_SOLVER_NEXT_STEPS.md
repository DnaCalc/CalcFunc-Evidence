# NPV kernel — offline search EXHAUSTED (2026-07-12 round 2)

A bounded 10-variant staging race (`check_npv_staging.rs`) plus an mpmath
correctly-rounded control settle the worksheet-NPV kernel identification as far
as offline analysis can:
- **Leader: plain-double reverse-Horner division `a=(a+c)/w`, 117/142 (cluster 36/47).**
  Three independently-staged reverse-Horner forms — pure SSE2, x87 `w` computed
  once, x87 `w` recomputed per statement — are **bit-identical** on every row.
  So NPV is x87-transparent (NOT a spill loop) and CSE-insensitive.
- **Ruled out:** reciprocal-multiply `(a+c)·(1/w)` (strictly worse, max|Δ|=3 —
  Excel does not precompute `1/(1+rate)`); forward running-product; integer-binexp
  pow; forward/reverse term summation; the `a/w + c/w` distributed split; and
  **extended-precision / correctly-rounded** accumulation (mpmath CR = 78/142,
  WORSE — NPV is genuinely plain double, not double-double).
- **Residual:** 25 rows (11 in the npvA cluster) at `±1..2` ULP, entirely in the
  cancellation regime (rates near the IRR root ~0.1634 where NPV≈0). Irreducible
  from offline re-staging. Needs DISCRIMINATING LIVE PROBES that isolate the exact
  plain-double accumulation order in cancellation (e.g. exact-cancelling cashflow
  designs), not more offline variants. **Solver family (IRR/RATE/YIELD/ODDFYIELD)
  is live-probe-gated here — deferred to a probe pass; cycle back.**

# IRR / NPV kernel state at 2026-07-12 session end

SCHEDULE (settled): FD-Newton in v = 1/(1+r); probe step ABSOLUTE
h = 1e-3 (sign under test; hneg led round 4); ladder rungs take >= 2
steps (lambda'^2 = 7.39e-7 = plateau); stop |dv| < tol (1e-7..1e-9
degenerate) with >= 1 applied step and apply-last; publish r = 1/v - 1
(stored reciprocal, exact subtract -> 8-ULP r-grid); f == 0 -> guess
passthrough. Racer: fit_irr_stores.rs (multi-step, 132/229 best).

KERNEL (open, the gate): worksheet NPV probed directly (142 rows:
answers-npv-r0/r1.json; n = 1,2,3,4,6 flows).
- 1-flow: division form matches everywhere.
- Leader: FORWARD per-term division chain t = t/w (extended), term c*t
  STORED, accumulate extended, w = 1+rate STORED -> 106/142.
- Residue: +-1..2 ULP on a quarter of multi-flow rows, all forms.
Ideas not yet tried: first-term special handling; range-iterator
accumulation order; per-term (1+rate) recompute with different store;
PC=53-with-extended-range subtleties; term as c*(t/w) vs (c*t)/w cross
associations; mixed spill masks per STATEMENT rather than per role.
Then: plug identified f into fit_irr_stores (f = cf0 + npv_kernel),
re-race schedule detail, expect closure of ladders + sweeps together.

RATE next after IRR closes (no passthrough; mandatory second seed).
Driver quirk: run ONE batch per PowerShell invocation (second batch in
the same session hits an Object[,] cast error in CellRefBatch).
