# NORMSDIST G-F3 wrapper / derived GAUSS

Date: 2026-08-21
Lane: W109 inverse-problem decomposition
Reference: Excel 16.0 build 20228, x64, Value2, Workbook Compatibility Version 2

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial` (wrapper and tiny-direct dataflow only)
- `target_completeness`: `target_partial`
- `integration_completeness`: `integrated` for the landed dispatch
- `open_lanes`: ERF/ERFC.PRECISE body (all numeric branches); GAUSS/NORMSDIST
  residual inherited from that body; tiny-route comb/grain after the G-A400
  dataflow; INV surfaces still on the Acklam/`libm::erf` refinement, not this
  wrapper

## Method

Related worksheet functions were asked, through cell `Range.Value2` inputs,
which public identity Excel actually computes. No Excel binary was inspected.
The wrapper identification is the 64/64 G-F3 ladder in
[`W109_ERF_SWARM_RESULTS_20260821.md`](W109_ERF_SWARM_RESULTS_20260821.md)
capture #4. Tiny-direct is the stored-z G-A400 family, 14/14 separators,
same-day capture #1.

## Identified graph

```text
z = |x| * RN(1/√2)                 // 0x3fe6a09e667f3bcd; divide-by-√2 refuted
Q = ERFC.PRECISE(z)                // still-open body
NORMSDIST(x<0)  = RN53(0.5*Q)      // then PHI-class DBL_MIN flush
NORMSDIST(x≥0)  = RN53(1 - 0.5*Q)
NORMSDIST(0)    = 0.5

GAUSS(x) = NORMSDIST(x) - 0.5      // ordinary route, abs(x) > 1e-15
GAUSS(x) = tiny-direct G-A400      // inclusive abs(x) ≤ 1e-15
```

Rivals refuted on the same ladder: `0.5+GAUSS` (H-F1) and the P-side
publication (H-F2). `NORMSDIST(-37.52) = +0` while same-sheet
`ERFC.PRECISE(z)` stays finite.

Tiny-direct dataflow (binary64 collapse of the racer Ext80 series): reuse
stored `z` as `w`, `g = 1+h` with per-op `gam1(½)` `h = 0x3fc06eba8214db6b`,
inner `0.5+(0.5-j)`, then `0.5 * (w*g)*inner`, signed, flushed.

## What was landed

`identified_std_normal_cdf` / `identified_gauss` in
`crates/oxfunc_core/src/functions/normal_log_family.rs`, consumed by
`NORMSDIST` / `NORM.S.DIST` CDF, `NORM.DIST` / `LOGNORM.DIST` CDF, and
`gauss_kernel`. Inverse surfaces keep the previous Acklam path
(`erf_based_cdf`) so INV bit pins do not ride the still-open ERFC body.

This is the same kind of landing as `CHIDIST(x,1) = ERFC.PRECISE(SQRT(x/2))`:
the identified public graph, on the still-open body.

## Current residual (not a wrapper miss)

At `z = RN(1/√2)` the production ERFC body is 1 ULP high versus live Excel
(same witness as `CHIDIST(1,1)`). The G-F3 paths then do:

| Surface | Excel bits | OxFunc vs Excel |
|---|---|---|
| `NORMSDIST(1)` / `GAUSS(1)` | `0x3feaec4bd120d37e` / `0x3fd5d897a241a6fc` | 0 ULP (`1-0.5*Q` absorbs the body ULP) |
| `NORMSDIST(-1)` / `GAUSS(-1)` | `0x3fc44ed0bb7cb209` / `0xbfd5d897a241a6fc` | 1 ULP (direct `0.5*Q` transports the body ULP) |
| `GAUSS(2^-50)` | `0x3cb9884533d43651` | 0 ULP (PHI(0) transport) |
| `GAUSS(2^-49)` | `0x3cc8000000000000` | 0 ULP (ordinary wrapper RNE) |
| `NORMSDIST(-37.52)` | `+0` | 0 ULP (flush) |

`GAUSS(1)` was previously 2 ULP (`0x3fd5d897a241a6fa` via `0.5*libm::erf`).
The remaining ±1-ULP NORMSDIST/GAUSS misses are the ERF/ERFC.PRECISE body,
not a second wrapper.

## Follow-up

Do not land 1-ULP near-identities for BINOM CDF, Poisson PMF, or a fitted
ERF body. The next high-leverage object is the ERFC body's relative-grain
exp/ln, with the swarm's hard constraints in the results note.
