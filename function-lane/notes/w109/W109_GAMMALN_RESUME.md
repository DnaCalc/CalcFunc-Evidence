# W109 GAMMALN — RESUME (residual-driven recovery)

Self-contained handoff to continue the GAMMALN custom-core recovery. Read this +
`W109_GAMMALN_IDENTIFICATION_20260711.md` + `W109_GAMMALN_PUBLISHED_COEFFICIENTS.md`.

## TL;DR state
- **Target:** Excel `GAMMALN` (≡ `GAMMALN.PRECISE` on build 20131, verified bit-identical)
  custom core on (0,11). Gates ~10 catalog rows (GAMMA, COMBIN, the G3-01 distributions).
- **Shape KNOWN (high confidence):** Cody/Boost minimax rational, **split at 1.5**,
  **D₁ = −γ** (near-1 = digamma(1)), form `lgamma(x) = xm·(D + xm·P(xm)/Q(xm))` (Cody) or
  `(x−1)(x−2)(Y + P/Q)` (Boost); ~3 rationals over (0.5,12) + Stirling above ~11 (Stirling
  already solved: plain-double Cephes tail + platform log, 136/139). Below 1: reflection.
- **Two unknowns, both now with a direction:**
  1. **coefficients** — recoverable to ~1 ULP (Gauss-Newton); netlib Cody's are already within ~1–2 ULP of Excel's.
  2. **op-graph** — family is **x87-EXTENDED**, identified via the residual noise floor.
- **Method: RESIDUAL-DRIVEN, not pass/fail.** Decompose the signed ULP residual
  `Excel(x)−eval(c,x)` into SMOOTH (moving-avg → coefficient/form error) + HIGH-FREQ
  (→ op-graph/rounding). Rank op-graphs by the noise floor; Gauss-Newton for coefficients;
  LLL for the last bit. Pass/fail is only the final gate.

## Current numbers, [1,1.5], 718 dense pts
- netlib Cody exact coeffs: 180/718, smooth 1.32, noise 1.41 ULP.
- Gauss-Newton-fitted (plain-double op-graph): **224/718, smooth 0.99**, noise floor 1.41.
- op-graph scan (fixed coeffs, ranked by noise): **x87 continuous 1.24** < x87 spill 1.27–1.29
  < ALL plain-double 1.41–1.58. → Excel evaluates in x87 extended precision.

## 2026-07-13 — SOURCE SWEEP exhausted (don't redo)
GitHub + literature sweep for a public source that could bit-match Excel's op-graph:
- **Provenance:** the Excel-2010 stats rewrite is undocumented at the algorithm level.
  The academic literature (McCullough; Mélard, *Comput Stat* 2014) only ASSESSES accuracy;
  no cited method / source. Microsoft's implementation is proprietary/internal.
- **Code sweep** (`gh search code` GAMMALN.PRECISE / gammaln): every public GAMMALN is an
  INDEPENDENT accuracy-oriented reimplementation — IronCalc, PhpSpreadsheet, formula.js,
  ClosedXML, LibreOffice Calc, HyperFormula, and Gnumeric (which uses its own `lgamma_rgnum`
  from R/GSL). None copies Excel; all are "right family" at most, never the exact op-graph.
  Gnumeric's Welinder — the deepest open-source RE of Excel stats — states Excel's source
  isn't available and does NOT bit-match it.
- **Conclusion:** consistent with the ≥2-rounding proof — the op-graph is what's needed and
  it is proprietary. No public source will bit-match. This path is CLOSED; GAMMALN stays
  legitimately open (NOT accept-divergence). The only untested corner is a specific
  proprietary BINARY (e.g. the msvcr90/100 CRT Excel 2010 shipped with) — but GAMMALN is
  Excel-internal 2010-rewrite code, not a CRT lgamma call, so even that is low-EV.

## 2026-07-12 UPDATE — stable Jacobian solved + DECISIVE reframing
- **Stable x87 Gauss-Newton — SOLVED (the prior blocker).** The finite-difference
  Jacobian through the x87 op-graph was quantized by the round-to-double steps. Fix:
  compute the Jacobian ANALYTICALLY at high precision (`stable_gn.jac`) — it is the
  derivative of the ideal real function, hence STAGING-INDEPENDENT and clean — while
  the residual uses the actual rounded op-graph, and fit the SMOOTHED residual (LM).
  Result on the x87 staging: smooth 1.30 → **0.42**, exact 138 → **240**. The analytic
  Jacobian is reused across all stagings (only `resid()` changes) → cheap enumeration.
- **Staging enumeration:** best is `poly0 rat0 prod0 sum1` = x87 poly/ratio/product with
  the `xm*rat + D` sum rounded to double before the outer multiply → **298/718** (noise
  1.234). All 16 Cody stagings floor at noise 1.21–1.34; none approach the ~0.29
  single-rounding limit.
- **DECISIVE free-fit test (`freefit.py`): Excel lgamma[1,1.5] has ≥2 internal roundings.**
  A free, arbitrary-degree Chebyshev fit of `g=lgamma/((x-1)(x-2))` (the best ANY smooth
  form could do) plateaus at **RMS 1.21 ULP / max 4.3 / ~248 exact** and does not improve
  past degree 14 (mean → 0). A single `round(smooth F)` would floor at ~0.29 ULP / ~100%
  exact. ⇒ **No smooth-form coefficient recovery (Cody/Boost/Lanczos/published) can be
  bit-exact.** This RETIRES the coefficient-hunt program. The mixed staging with an extra
  inner rounding (298) already beats the free smooth fit (248), confirming ≥2 roundings.
- **Endgame is now:** identify the exact multi-rounding op-graph (which intermediates
  spill to double), then CVP the coefficients. Correct-staging signal = misses collapse to
  <1 ULP pre-round (`miss_diagnostic.py`). Best staging so far still has 80% of misses
  >1 ULP → staging not yet exact. `mixed_scan.py` ranks stagings by this CVP-viability.
- Harness added: `stable_gn.py`, `staging_scan.py`, `inner_scan.py`, `miss_diagnostic.py`,
  `freefit.py`, `mixed_scan.py`, `refine_staging.py`, `cvp_refine.py` (all in work dir).

## Files (harness + data live in the GITIGNORED work dir, on local disk)
Dir: `smart-fuzzer/work/w109/G3-02-gamma/`
- **Data** (live Excel, gzipped-cacheable): `answers-g12dense.json` (1468 dense (1,2) + adjacent-double
  clusters), `answers-dense1.json` (1016 over (0.1,11.5)), `answers-peel.json` (399 exact-offset
  x=1+m·2⁻ᵏ), `answers-precise.json` (GAMMALN.PRECISE check).
- **Harness:** `lgamma_recover.py` (load_band, fits, staged eval, PSLQ id — note `identify_constant`
  tol is 1e-25, widen to ~1e-15), `residual_harness.py` (`decompose()` smooth/noise, op-graph variants,
  netlib Cody coeffs D1/P1/Q1), `gn_fit.py` (Gauss-Newton per op-graph → floors), `opgraph_scan.py`
  (noise-floor ranking), `cody_exact.py` (netlib Cody all ranges), `boost_test.py` (exact Boost),
  `fdlibm_x87.py` (fdlibm tc-branch). Rebuildable from the coefficient doc if lost.
- **Exact coefficients** (tracked): `W109_GAMMALN_PUBLISHED_COEFFICIENTS.md` (netlib Cody D1/P1/Q1,
  D2/P2/Q2, D4/P4/Q4, Stirling C; Boost Y/P/Q per sub-range).

## Next steps (in order) — REVISED 2026-07-12 post-freefit
1. ~~Stable x87 Gauss-Newton~~ **DONE** (`stable_gn.py`, analytic staging-independent Jacobian).
2. ~~Prove single-vs-multi rounding~~ **DONE** (`freefit.py`): ≥2 roundings; smooth-form recovery
   is impossible. Coefficient-hunt program retired.
3. **Identify the exact multi-rounding op-graph.** Enumerate mixed-precision stagings (which of
   {poly-per-step, ratio, xm·rat, +D, final} round to double vs stay x87-extended; division vs
   x87-reciprocal; Cody `xm*(xm*R+d1)` ordering). Rank by CVP-viability = fraction of misses with
   pre-round |dist|<1 ULP (`mixed_scan.py` / `miss_diagnostic.py`), NOT exact count. The correct
   op-graph is the one whose misses collapse to <1 ULP.
4. **CVP the coefficients** on the pinned op-graph (`cvp_refine.py` / `refine_staging.py`): the
   remaining <1-ULP misses are integer coefficient-ULP nudges. Upgrade to real LLL (fpylll) if
   coordinate/Babai polish stalls.
5. **If step 3 finds no <1-ULP-collapsing staging:** the op-graph is more exotic (e.g. a different
   algorithm/precision than Cody-rational, or an SSE2/x87 mix per subexpression the current
   parametrization can't express). Per the "don't get stuck" rule: write up the residual structure
   (mixed_scan ranking + where structural misses concentrate), design the next probe, and cycle to a
   higher-leverage lane (PMT/MINVERSE/ACCRINT/solver), returning later.
6. **Extend** to [1.5,2] (reflected `(2−z)(1−z)(Y+R(2−z))`) and [2,3]; then compose
   GAMMA = exp(lgamma) (+ sin reflection for negatives), COMBIN, and re-race the G3-01 distributions.

## Commands
```
cd /c/Work/DnaCalc/OxFunc/smart-fuzzer/work/w109/G3-02-gamma
python3 residual_harness.py   # op-graph decomposition (smooth/noise)
python3 gn_fit.py             # Gauss-Newton per op-graph + residual floors
python3 opgraph_scan.py       # op-graph staging ranked by noise floor
```
Harvest more probes (from repo root, PowerShell, ONE batch per invocation):
`.\smart-fuzzer\tools\Run-W109ProbeBatch.ps1 -Batch <batch.json> -Out <answers.json>`
(ProbeBatch format: `{function, probes:[{probe:{id, args:[bits_hex]}}]}`; `result_index` is 1-based.)

## Method note (durable, transferable)
For a bit-exact inverse problem, pass/fail match-count is a near-flat, information-destroying objective.
Use the SIGNED residual and its STRUCTURE: SMOOTH component = coefficient/metric/form error (drive with
Gauss-Newton on the Jacobian), HIGH-FREQ component = op-graph/rounding (enumerate op-graphs, rank by the
noise floor). The floors diagnose which unknown is binding and give each a continuous gradient. See
`[[residual-structure-not-passfail]]`.
