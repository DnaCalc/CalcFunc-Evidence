# ERFC body attack plan (public sources only)

Date: 2026-08-23
Lane: W109 inverse-problem / calc-graph search
Parent: `W109_ERF_SWARM_RESULTS_20260821.md`

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial` (G-F3 / G-A400 wrapper integrated;
  ERFC body still scaffolding)
- `open_lanes`: ERF/ERFC.PRECISE body; GAUSS/NORMSDIST residual inherited from
  that body; tiny-route comb/grain; sealed heldouts untouched

This is an attack plan plus a named-graph race, not a body identification.
Do not land a 1-ULP near-identity or a fitted `libm*(1+corr)` table.

## Clean-room bounds

Allowed: public specifications, published research (Cody 1969 / SPECFUN,
NSWC TR 92/425, fdlibm, Cephes, Boost-era headers already in-tree), and
reproducible Excel `Range.Value2` banks already frozen.

Forbidden: disassembly, decompilation, or inspection of Excel or any
Microsoft-shipped binary. Do not open `answers-b9heldout.json` or either
GAUSS heldout.

## What the swarm already proved (do not re-prove)

1. One body. ERFC.PRECISE, CHIDIST(2z²,1), and GAUSS-decoded Q agree
   330/330.
2. Complement direction flips at exactly 0.5: below, Q = RN53(RN64(1−P))
   (x87 spill, capture #5); above, P = RN53(1−Q). No 1.375 seam.
3. Tail staging is unsplit `exp(−RN53(z·z))`, per-op binary64 E·F, PHI-class
   DBL_MIN flush. Split-argument exp (fdlibm/Cody AINT/16) is dead.
4. Best *named* tail so far: Cody-1969/SPECFUN rationals with unsplit exp,
   3,218/3,557 on the GAUSS tail composite; family ceiling 3,273 / 146/355
   direct. Cody is not at the ceiling. Next named candidate: NSWC
   double-precision DERFC1 / DERFC0 (TR 92/425), which is **not** the
   already-killed CDFLIB `erfc1.f` helper.
5. F-body pin witnesses (units 2⁻⁵³ rel of F after unsplit-w):
   z = 0.75 → −3.73, 1.28125 → +4.17, 1.875 → −7.09, 2.125 → −4.56,
   5.0 → −5.41.
6. Small-z (z<0.5) is P-side. Branch-190 dataflow with extra RN53 stores;
   per-op `gam1(½)` h = `0x3fc06eba8214db6b`; inner cluster RN53-staged.
   The remaining object there is the mantissa comb, not a second wrapper.

## Attack order

### A. Named F race (this session)

Race public tail graphs on frozen ERFC.PRECISE discovery banks
(`answers-erfcp/erfcm/b7erfc/b8erfc/b11c.json`) plus the implied-Q bank
`answers-b24-normref.json` (Q = 2·NORMSDIST exactly on all-negative x,
z = |x|·RN(1/√2)). Score by band: z<0.5, [0.5,4), [4,26.543), flush.

Candidates, all with unsplit `excel_exp(−RN53(z·z))` unless marked split:

| Graph | Source |
|---|---|
| `libm::erfc` | host control |
| production `erfc_precise_kernel` | fitted scaffolding, not an ID |
| Cody CALERF jint=1 | SPECFUN, **split** exp (negative control) |
| Cody erfcx · unsplit host exp | SPECFUN F, host exp |
| Cody erfcx · unsplit `excel_exp` | SPECFUN F, identified Excel EXP |
| NSWC DERFC / DERFC0 · host exp | TR 92/425, jacobwilliams/nswc |
| NSWC DERFC0 · unsplit `excel_exp` | same F, identified Excel EXP |

A graph is a survivor only if it is bit-exact on a band, or matches the
five F-body pins *and* beats Cody-unsplit on that band without adding
error on already-exact rows. Anything else is a kill or a constraint.

### B. If a named F is close but not exact

Do **not** fit a correction polynomial. Do:

1. Last-bit coefficient scan of the published decimals (the GAMMALN
   lesson: Excel sometimes uses the same form with a rounded-or-refit
   constant). One ULP per coefficient, one coefficient at a time, on the
   pin witnesses first.
2. Association / store-site race of the winner's Horner (per-op RN53 vs
   x87 PC64 vs stage-spill), same style as `race_erf_precise_public_small`.
3. Cut-point race: Cody 0.46875 vs Excel 0.5; NSWC 1 / 2 / 4 / 50.

### C. Small-z body, only after A/B

The tiny comb is not a second ERFC. It is the same relative-grain object
seen on the tail F residual. Do not invent a new tiny-only constant.
If a named F dies, the small-z work stays on extra RN53 stores in
branch 190 (already constrained) rather than a new rational.

### D. What would count as an identification

A public evaluation tree, with published coefficients (or a documented
one-ULP rounding of those decimals), that reproduces Excel ERFC.PRECISE
bits on the frozen discovery banks, including the five F pins, the
complement-direction law, and the PHI-class flush. Then, and only then,
land it under the CHIDIST(df=1) pattern: identified graph on a now-known
body, with heldouts still sealed until a promotion gate.

## Racer

`smart-fuzzer/tools/calc_graph_racer/src/bin/race_erfc_named_f.rs`

Usage, from that crate:

```
cargo run --release --bin race_erfc_named_f -- ../../work/w109/G3-01-dist
```

## Session outcome (2026-08-23)

Named-F race ran on 15,556 frozen z rows. Full table:
[`W109_ERFC_NAMED_F_RACE_20260823.md`](W109_ERFC_NAMED_F_RACE_20260823.md).

Headline: NSWC DERFC1 with unsplit `excel_exp` is the new named leader
(5371/15556) and beats Cody-unsplit (5095) and libm (3406). **Not an
identification.** Cody C/D ±1 ULP is a ±14-row wiggle, not a last-bit
hit. Production corr-fit is worse than libm on this corpus. No landing.

Plan A and B.1 executed 2026-08-23 (named F + Cody ±1 ULP). Sequential
tests 1–3 executed the same day; see
[`W109_ERFC_NAMED_F_RACE_20260823.md`](W109_ERFC_NAMED_F_RACE_20260823.md).

| Test | Result |
|---|---|
| 1 NSWC Horner / cuts | x87-continuous + store `u/v` + cuts 0.5/1.5 → 6127/15556, pins 2–4 ULP. Constraint, not ID. |
| 2 SLATEC/MATH77 Chebyshev | 5149–5296/15556. Killed as the body. Small-z Chebyshev 1419/1864 is the best named P-side series, still not exact. |
| 3 branch-190 extra RN53 stores | `check_erf190` ceiling 850/1508 P-side; inner A vs B tied; leftover comb. No new constant. |

Body remains unidentified. Do not land.

### Firehorse store-mask cubes (96h cap, 2026-08-27)

Full note: [`W109_ERFC_CAMPAIGN_FIREHORSE_20260823.md`](W109_ERFC_CAMPAIGN_FIREHORSE_20260823.md).

All six R1m 26-bit PQR+t cubes (mid_cut=1.5, every zz_dr × uv association)
finished. Best mid **3336**/7741 max 7 ULP (`R1m/z0/r0 mask=0x0048000`),
+4 over the named bar, pins still inexact. Remaining R1 26-bit axes skipped after `R1/z0/r0`. R4 (all six AA/BB
19-bit), R2 (all six Cody 16-bit), and R0aabb (±1 ULP AA/BB/E) finished
2026-08-31 with **no scoreboard move** (3336/7741, 7 ULP, 0 pins).
Store-site / last-bit on NSWC and Cody F is exhausted. Implied-F race of
Cephes, fdlibm, NSWC CC/DD, and A&S/Gautschi CF (2026-08-31): none is
the body; NSWC still leads mid 2388/7741 max 7; CF A&S leads tail exact
1283/5934 with the same 189 ULP ceiling. `F_or` rebuilt under identified
w: native vs x87-DR square differs on 3/13687 rows (pins unchanged, mid
ceiling still 7 ULP); split-exp `w` dies. Leftover is F, not w. Still
not an identification. Do not land.