# W109 GAMMALN — Op-Tree Shape Corpus (GitHub-sweep-seeded)

Harvested 2026-07-13 by the `gammaln-optree-harvest` workflow (20 lgamma implementations
extracted to op-tree structure, then synthesized). Rationale (per the reframe): the freefit
proof says Excel's GAMMALN[1,1.5] op-graph is OUTSIDE the Cody rational family and has ≥2
internal roundings, so the SHAPE (which determines the rounding sites), not the coefficients,
is what we must match. This corpus is the empirically-complete shape space — how ~20
independent authors actually structured lgamma near 1. Coefficients are refit per shape via
the generic stable fitter (`generic_fit.py`, high-precision numerical Jacobian). Full data:
`smart-fuzzer/work/w109/G3-02-gamma/optree_corpus.json` (+ `optree_synthesis.txt`).

## Decisive structural discriminator: EXACT ZEROS (VERIFIED)
Live-Excel probe (build 20131, cache-confirmed): `GAMMALN(1)` → `0x0000000000000000`,
`GAMMALN(2)` → `0x0000000000000000` — **exactly +0.0** (sanity: `GAMMALN(3)`=ln2
`0x3fe62e42fefa39f0`, `GAMMALN(0.5)`=ln√π `0x3fe250d048e7a1bd`). Shapes that produce the
zeros by **cancellation** (residual ~1e-9), not an algebraic factor, are therefore EXCLUDED:
NR Lanczos, LibreOffice Lanczos-then-log, Gnumeric power-series, Nemes/Windschitl Stirling,
R Chebyshev-then-log. ⇒ Excel is an **algebraic-factor rational** (a structural `(x-1)`/
`(x-1)(x-2)` factor or a top-level purge-to-0), which narrows the race to the rational family.

## Shapes (13 distinct, vs the raced Cody baseline `xm*(D + xm*P/Q)` = 298/718)

### Algebraic-factor rationals (candidates — exact zeros compatible)
- **DCDFLIB/TOMS708 `gamln1`** — bare `-a·(P/Q)`, a=x-1, monic Q, **no inner D, no outer xm
  multiply**; Euler-γ folded as numerator `p0`; negate last. (team best-of 174/1468 refit).
- **AS245 (Macleod)** — rational in the **UNREDUCED** argument `y=x` (Horner over [1,1.5]),
  zero-factor multiplied in as `(xm·Num)/Den` before the divide; monic (4,4), no D.
- **Boost `lgamma_small_imp`** — `(z-1)(z-2)·(Y + P/Q)`, **two** zero-factors, fat float `Y`
  outside the ratio, **distributed** final `prefix·Y + prefix·R` (2 mul, 1 add). Cut at 1.5.
- **fdlibm lower branch** [1,1.2316) — `(-0.5·y) + P/Q`, y=x-1, numerator `y·U(y)` (explicit
  y factor), monic denom, linear term ADDED OUTSIDE the ratio, no outer multiply.
- **fdlibm upper branch** [1.2316,1.5] — PURE POLYNOMIAL about the interior minimum
  `tc=1.46163214496836224576`, offset by a **double-double (tf,tt)** center constant (tt
  subtracted inside → built-in 2nd rounding), 3-stream mod-3 Estrin recombination. Split.
- **GSL `lngamma_1_pade`** — root-FACTORED (2,2) Padé `(eps+n1)(eps+n2)/((eps+d1)(eps+d2))`
  with leading `K`, plus an additive `eps^5` correction, all ×eps.

### Log-in-the-body / cancellation-zero shapes (EXCLUDED by exact zeros, kept for record)
- **Cephes** `log(1/x) + w·B(w)/C(w)` (reciprocal-then-log, recurrence-shifted rational).
- **Apache/Hipparchus** `-log1p(xm1·c(t))`, c a deg-14 Horner seeded at top by a P/Q rational.
- **R Nmath** Chebyshev/Clenshaw → `log(Gamma)`; **NR** Lanczos sum-of-poles + 2 logs;
  **LibreOffice** Lanczos in 1/x → pow/exp/log; **Gnumeric** 40-term zeta power series +
  log1pmx via Lentz continued fractions; **Nemes/Windschitl** Stirling-in-1/z² + logs.
  (All go through the x87 87tran chain on the Excel host — relevant ONLY if the exact-zeros
  premise were wrong.)

## Race results ([1,1.5], 718 pts; each shape stable-fit, x87 vs per-op double)
Baseline: **Cody rational (deg 8/8), x87 = 298/718** (smooth 0.50, noise 1.23).
Machinery: `generic_fit.py` (high-precision numerical Jacobian, staging-independent) +
`shapes_corpus.py` (each shape = one `shape(c,x,exact)`; trailing-monic mpmath rational seed).

Native-degree harvested rationals (`shapes_corpus.py`, seed rel-err 1e-14..1e-13):
| shape | native deg | staging | fitted smooth (ULP) | note |
|---|---|---|---|---|
| DCDFLIB `gamln1` | 6/6 | x87 & dbl | ~52 | dbl==x87 to <0.1 |
| Boost `(z-1)(z-2)(Y+P/Q)` | 5/6 | x87 & dbl | ~439 | dbl==x87 |
| fdlibm lower `(-0.5y)+P/Q` | 5/6 | x87 & dbl | ~616 | dbl==x87 |

**Result: CONFOUNDED / inconclusive.** These shapes' NATIVE degrees are lower than Cody's
8/8, so their APPROXIMATION error (52–616 ULP) dominates and completely masks the ~1 ULP
rounding-structure difference we want to measure — proven by `dbl` and `x87` stagings giving
*identical* smooth/noise per shape. No structural signal, and no breakthrough vs Cody's 298.

**Required next step — the DEGREE-NORMALIZED structural race:** re-race every algebraic-factor
shape at a COMMON high degree (≥8/8) with a converged fit, so all reach ~0.5 ULp smooth (Cody's
level) and ONLY the op-tree rounding structure differs. Then the exact-bit count isolates which
STRUCTURE best matches Excel's ≥2-rounding op-graph. Strong prior (deep wall + prior-workflow
~40% + the freefit single-rounding ceiling ~248) says none will exceed ~40% — but this is the
principled test the corpus was harvested for, and it closes the shape-coverage question.
Also pending: fdlibm UPPER (tc-polynomial + double-double) on its [1.2316,1.5] sub-band; GSL
factored-Padé. (The log/Lanczos/cancellation shapes are excluded by the verified exact zeros.)

## DETERMINISTIC RESIDUAL DECODE (2026-07-13, "there is no noise")
The high-freq residual is a DETERMINISTIC signal, not noise: for a fixed op-graph
`Excel(x)=round(F_real(x) + Σ_{k∈S} shift_k(x))`, where `shift_k` = the sensitivity-weighted
rounding-error SAWTOOTH of intermediate `T_k`. Tools: `residual_decode.py` (regress δ on the
spill basis + spill-subset scan), `delta_shape.py` (profile δ across the band), `split_test.py`.
Findings on the best Cody sum-spill model (coeffs fit so smooth≈0):
- **Pre-final residual δ: rms 1.28, smooth 0.43, max|δ| 4.6** — deterministic, NOT bounded <0.5.
- **δ is HIGH-FREQUENCY** (lag-1 autocorr +0.07, 46% sign-flips) — bit-level structure, not a
  smooth form gap; its **ULP-amplitude GROWS toward the upper band** (rms 1.0→1.7 as x:1→1.5,
  ~4-ULP peaks in [1.25,1.5]). "Not fractal" — the amplitude has real structure.
- **None of the 5 intermediate spills explain it**: corr(δ,shift_k) ≤ 0.08 for xn/xd/ratio/
  t/inner; regression β all 0.14–0.27 (none ≈1); NO spill-subset drives max|δ|<0.5 (best
  {inner} max 4.28). The confound: **sawtooth PHASE depends on the coefficients**, and fitted
  coeffs ≠ Excel's exact doubles, so op-graph and coeffs are entangled in every observation.
- **Split at 1.2316 rejected as the primary structure**: band-specific coeffs cut only the
  SMOOTH part (0.48→0.23 lower, 0.29→0.20 upper; exact 136→150, 158→167) — the **noise floor
  stays ~1.0/1.4 regardless of split**. The ≥2-rounding structure is intrinsic per sub-band;
  the upper band is coefficient-independently noisier.
- **Frontier:** the exact structure is the JOINT (x87 register-spill pattern × exact double
  coefficients) — a large combinatorial × lattice problem. Natural candidate spaces (5 spills,
  coeffs, split) are exhausted without closing it. To break the coeff-phase confound: EXACT-
  ARITHMETIC probing (choose x where a target intermediate is exactly representable, isolating
  one rounding), or a joint spill×CVP search over a much larger spill-pattern space.
