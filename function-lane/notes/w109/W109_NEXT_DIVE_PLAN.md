# W109 — Next Dive Plan (post-GAMMALN pivot, 2026-07-13)

GAMMALN core is DEFERRED (fully characterized op-graph wall; see W109_GAMMALN_*). Pivoting to
the other open lanes. This plan is from the parallel lane survey (`w109-lane-survey` workflow);
full data in `W109_LANE_SURVEY_20260713.json`. Session tools available:
deterministic-residual-decoder, held-out-ceiling test, op-tree-harvester, generic stable fitter
(all in `smart-fuzzer/work/w109/G3-02-gamma/`), Welinder digest.

## DO FIRST — banked quick win (near-zero risk): MINVERSE landing
The shipping kernel `matrix_family.rs::inverse_kernel` STILL runs the RULED-OUT Gauss-Jordan
(≈80/159 live) — the catalog "already implemented" note is wrong (verified this session at
`matrix_family.rs:180`). The correct algorithm is already identified AND held-out-validated:
**Doolittle-LU partial-pivot + per-column unit-vector solve + division-form back-sub, plain
float64** (150/159 3x3, 103/108 held-out, 448/448 4x4). Staging in
`scratchpad/minverse_combined.py::dl()`; `determinant_kernel` (line ~134) already has the LU
elimination. **Swap it in**, re-run `matrix_local_eval` + the W097 R-F resweep as the regression
gate, re-run the held-out ceiling. Banks ~70 cells + removes 3 spurious #NUM. (Residual 9-cell
+1-ULP near-cancellation stays as a separate decoder probe.)

## THEN — recommended DIVE: YIELD / ODDFYIELD (G6-03/04)
**UPDATE 2026-07-13 — this premise was WRONG.** The forward `pcomp` price kernel is NOT
bit-exact: it computes `base^(off+k)` with `base.powf` (Rust powf = `exp·ln` even for integer
exponents) but Excel uses the C-runtime `pow` integer special case = **binary exponentiation**.
Identified + held-out validated (25 live-Excel PRICE pts / 5 bonds, 15/15 + 10/10). YIELD is a
forward-kernel binexp fix PLUS a plateau-publication schedule (COUPLED — land together; pcomp
fix alone regresses YIELD-par 6→~40 ULP). PRICE has latent binexp drift too. Full writeup:
`work/w109/G6-solvers/YIELD_PRICE_FORWARD_KERNEL.md`; catalog G6-03/03b/04 updated. Original
(now-corrected) text follows:

Forward `pcomp` (YIELD, `bond_core_family.rs`) and `oddfprice_kernel` (ODDFYIELD,
`odd_bond_family.rs`) are ALREADY bit-exact, so 100% of the residual is the ~15-line inversion
SCHEDULE. First experiment needs **zero new Excel capture**: implement the classic
ATP/LibreOffice false-position yield schedule in Rust (y1=0,y2=1, seed prices, interval-doubling,
**exact-price-equality early-exit**, cap 100, publish final iterate) over the existing x87 V/Ext80
kernels, and run against the 4 existing witnesses (`DISCREPANCY_RECON_RESULTS_20260710.csv:32-35`,
2 YIELD + 2 ODDFYIELD). Target the two PAR witnesses that pin the early-exit (YIELD-par must return
EXACTLY `0x3fa999999999999a`). If the 4 bits reproduce: ODDFYIELD ~3e5 ULP → 0, YIELD 6–19 ULP → 0.
Then capture a held-out price-ladder before promotion. This also builds the solver-VM for RATE+IRR.

## Lane ranking (dive-target)
1. **YIELD/ODDFYIELD** — best dive (kernels closed, 0 new capture, closes 2 fns, builds solver-VM).
2. **MINVERSE** — highest-certainty close (land + rescore); do in parallel, don't gate behind YIELD.
3. **ACCRINT (G6-02)** — close: 1 ULP on 1 witness; Excel accumulates settlement-first/BACKWARD;
   mirror the already-exact odd-coupon branch. Needs held-out settlement>first battery (g6-threeway COM).
4. **CONVERT (G4-05)** — op-graph known (`value*Cfrom/Cto`, extended >53-bit factors); 1/1 witness =
   overfit; needs text-arg plumbing (~5-line CellRefBatch branch) + 2^k reveal sweep.
5. **RATE (G6-05)** — f-kernel CLOSED (FV 149/149); schedule fully unpinned; NO rate racer exists yet.
6. **TREND/LINEST/LOGEST/GROWTH** — cheap correctness win (reroute to centered kernel 1/12→7/12);
   bit-exact slope is a GAMMALN-class wall, under-determined by 4 datasets.
7. **IRR+NPV (G6-06)** — worst dive for a *close*: GAMMALN-class last-ULP wall at accumulation
   depth≥3 (rounding+precision axes proven dead); NPV witnesses ARE the IRR f-evals. Decoder probe.

## Machinery to build (ranked by cross-lane leverage)
1. **Solver-VM racer** — one x87 V/Ext80 iteration harness feeding a bit-exact forward kernel;
   pluggable {update: false-position/secant/FD-Newton/bisection} × {stop: exact-equality/|dv|<tol/
   |dv|-vs-h/|f|-staging-true/fixed-count} × seed × probe-sign × cap × published-iterate. Serves all 4 G6 solvers.
2. **Held-out ceiling harness** — universal promotion guard (burned PMT 36/48→57%, MINVERSE 51/51→147/159).
3. **Deterministic residual decoder** — emit signed IEEE-RN sawtooth per add/divide, regress + subset-scan
   the offending op. Serves NPV depth≥3, MINVERSE 9-cell, TREND slope, RATE arithmetic, CONVERT.
4. **Live-Excel harvesters** — YIELD price-ladder, NPV n=5/7, RATE guess/#NUM! ladder, ACCRINT battery, CONVERT 2^k.
5. **Text-arg plumbing** — ~5-line `[string]` branch in `CellRefBatch.psm1 _New-ScalarArgValueArray` (unblocks CONVERT/EUROCONVERT).
6. **Metamorphic / 2^k-invariance battery** — fingerprints accumulator+centering (TREND) and stored-constant precision (CONVERT) with no code access.
7. **Back-out-effective-(a,b) extractor** — recover Excel's exact slope/intercept from ≥3 collinear published values (TREND).

## Best generalizable IDEAS (harvested)
- **Forward-kernel-first factoring:** once the forward kernel is bit-exact, inversion collapses to a ~15-line schedule search. Factor every solver as (kernel, then schedule).
- **Kill the rounding/precision axis first:** prove SSE == RN53(RN64) bit-identical (and test extended — usually worse) to collapse candidate axes BEFORE op-graph hunting (killed 3 axes on NPV+MINVERSE).
- **Minimal-n degenerate witness** (n=1 makes f LINEAR) isolates schedule from kernel — seed/step/publish fall out (RATE 72-ULP identity, YIELD par).
- **Publish the RAW final iterate**, never a polished/bisected/nearest root (RATE 72-ULP identity; YIELD-par lands exactly on coupon). Invalidates OxFunc's current bracket+bisection RATE and both bisection YIELD/ODDFYIELD.
- **Mantissa-entropy fingerprint:** trailing-zero low bits (`0x…bc4000`) ⇒ premature/coarse stop; full-entropy mantissa ⇒ converged. Cheap converged-vs-not discriminator, no reference needed. Par/economic-root witnesses fingerprint the exact-equality early-exit.
- **Verify the shipping kernel actually implements the "identified" algo** (source + git) before trusting a catalog note — MINVERSE hid a ~44% live gap behind a "9-cell +1 ULP" framing.
- **+1-ULP on mixed-magnitude / near-cancellation / small-determinant = accumulation-ORDER fingerprint**, not approximation error — enumerate finite orderings in pure double BEFORE x87/extended (NPV, MINVERSE, ACCRINT).
- **Mirror-branch porting:** when two branches handle mirror regimes, port the bit-exact one's op-order to the other (ACCRINT odd-coupon → forward branch).
- **Power-of-two exact-rescale** reveals a stored constant's sub-double bits + divide rounding mode without perturbing rounding; forward-multiply-exact / reverse-divide-±1-ULP asymmetry is a cheap >53-bit-constant detector (CONVERT, day-count).
- **Couple a solver's f-corpus to its own root** (dense sweep around the root) so the kernel witnesses ARE the solver's evaluations — kernel and schedule close together (NPV↔IRR).
