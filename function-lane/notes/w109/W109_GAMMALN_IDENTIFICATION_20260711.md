# W109 Phase-5: GAMMALN identification — Stirling region identified, small-x core scoped as custom

Live oracle: Excel 16.0 build 20131, x86-64 AMD host. Corpus: 361 distinct
positive GAMMALN answers (93 legacy + 274 fresh probes in
`smart-fuzzer/work/w109/G3-02-gamma/answers-r2.json`: dense grids on (0,1)
step 0.02, (1,3) step 0.04, (3,9.5) step 0.11, (9.5,13.5) step 0.05, plus
near-1/near-2 cancellation ladders and boundary pairs).

## Identified: the asymptotic region (x ≥ ~11)

Excel's GAMMALN for `x ≥ 11` is the **plain-double Cephes `lgam` Stirling
tail with a platform-class (UCRT) log** — no x87 anywhere:

```text
q  = (x - 0.5)*log(x) - x + 0.91893853320467274178      (plain double, left-to-right)
p  = 1.0/(x*x)
t  = polevl(p, A5)          A5 = Cephes lgam A[] table (5 coefficients)
r  = q + t/x
```

Score: **136/139 bit-exact on every row x ≥ 11** (11–1030). The three
residual rows (x = 11.3 +1 ULP, 12.75 −1 ULP, 91.608499 +1 ULP) are
attributable to Excel's statically-linked CRT `log` differing from the
host UCRT `log` by <1 ULP on those arguments (each flip requires only a
~0.3–0.7 ULP shift of `log(x)`; no FMA/association/coefficient variant of
the surrounding arithmetic moves them, and the same formula with fdlibm's
log scores worse, 132/139).

Notes:
- The earlier "83/83 x87-staged Stirling" result (commit 8b57a49 era) was
  an over-fit: 8 free store-mask bits against 83 rows ≥ 13.19. The dense
  10–13.5 probes kill every x87 staging; plain double + platform log is
  the unique survivor and needs **zero** free bits.
- The x = 11.0 witness (`GAMMALN(11)=0x402e357590954d16`) is 1 ULP ABOVE
  the correctly-rounded ln(3628800) — impossible for any log staging of an
  exact-product reduction, natural for Stirling truncation. This was the
  probe that broke the small-path assumption.

## Boundary

The small/Stirling switch sits in **(10.25, 11.0]** — Stirling matches
nothing below 10.25 (0/25 on [8,10)) and everything from 11.0 up.
Exact threshold pinned next by adjacent-representable bisection (~40 live
probes).

## The small-x core (0 < x < ~11): custom Microsoft rational

Facts established from the dense corpus:
- Accuracy vs true lgamma: ≤ 3.5 ULP everywhere; sub-ULP on (3,10);
  ±3 on (0.9,3); ±2 on (0,0.9). NOT correctly-rounded quality → genuine
  plain-double rational arithmetic, NOT extended/x87.
- `GAMMALN(1) = GAMMALN(2) = 0` exactly (anchored or special-cased).
- `GAMMALN(3)` is 1 ULP above CR(ln 2) → the region does real arithmetic
  even at integer points (no `log(z)+0` early-out).
- Below ~0.5 the form is `-log(x) + (accurate poly)` with a platform-class
  log (fdlibm-structure scores 32/34 there; the poly's own error is
  magnitude-masked).
- On (0.68,4), where a core polynomial is bit-exposed, **every public
  implementation fails at the coincidence baseline (~50%)**.

Ruled out bit-exactly (plain double + FMA + x87 spill + extended stagings,
platform/fyl2x/fdlibm logs as applicable):

| candidate | best score | killed by |
|---|---|---|
| Cephes lgam small path (B/C rational), all 128+ stagings, ln in/out stores | 52 rows unexplainable | dense (0,3) grid |
| Recurrence-to-Stirling, T ∈ 4..16, log-of-product AND sum-of-logs, all stagings | 174/361 max | anti-correlates below 11 (14/220 at T=11 plain) |
| fdlibm `__ieee754_lgamma_r` (full, incl. fdlibm log, FMA variants) | 203/361 | naked-poly bands (0.9,3): 9/40, [2,3): 7/28 |
| UCRT `lgamma` (ucrtbase.dll direct) | 192/361 | scattered ±3 |
| R / SLATEC Fullerton (gamcs Chebyshev, lgammacor) | 177/361 | (0,10) gamma-then-log profile wrong |
| Cody SPECFUN DLGAMA (P1/P2/P4, C-array) | 178/361 | all bands baseline |
| DCDFLIB / NSWC gamln + gamln1 (TOMS 708) | 174/361 | (0.8,2.25]: 6–12 ULP misses |
| AS 245 (Macleod ALNGAM) | 74/361 | 12-digit coefficients → 1e-9 relative; Excel is ~1e-16 |
| GSL Lanczos g=7 | 63/361 | everywhere |
| NR gammln (Lanczos g=5) | 1/93 | 45k ULP (prior session) |
| Boost lgamma_small_imp (64-bit variant used for double) | 131/280 (<15) | all bands baseline |
| Cephes `gamma()` (P/Q + stirf) for worksheet GAMMA | 8/79 positive | growing ULP with x |
| GAMMALN = log(published GAMMA bits) | 37/79 | near-1 rows |
| UCRT tgamma for worksheet GAMMA | 13/156 | everywhere |

Conclusion: the (0,11) core is a **custom Microsoft implementation**
(consistent with the Excel 2010 "function accuracy improvements" rewrite)
— likely a banded rational re-fit that no public source matches. The
worksheet GAMMA errors grow with x like `exp(lgam-with-absolute-error)`,
so GAMMA is expected to be `exp` over this same internal lgamma; COMBIN
and the G3-01 distributions sit on the same substrate. **Identifying this
one custom kernel remains the gate for the whole gamma family.**

## 2026-07-12 live-probe harvest — the (1,2) FORM identified

Live pipeline re-validated (GAMMALN(11)=0x402e357590954d16, GAMMALN(1)=GAMMALN(2)=0)
and a 1016-point dense batch harvested over (0.1, 11.5) into
`answers-dense1.json`. Error-vs-true(mpmath) ULP profile by band:

| band | ULP err | note |
|---|---|---|
| (0.1,0.5) | ±1 | near-correctly-rounded (`-log(x)+poly` regime) |
| (0.5,1.0) | ±2 | |
| (1.0,1.5) | −3..+5 | polynomial EXPOSED |
| (1.5,2.0) | −5..+2 | polynomial EXPOSED |
| (2.0,3.0) | ±4 | exposed |
| (3.0,6.0) | ±1 | accurate again |
| (6.0,10) | −3..+1 | |
| (10,11.5) | ±2 | Stirling region |

The error curve is a SMOOTH ±few-ULP oscillation, NOT piecewise — the apparent
"edges" are just the approximation error oscillating, so there is no hidden
sub-band structure in (1,3).

**KEY: the (1,2) form is `lgamma(1+s) = s·(s−1)·P(s)`** (s = x−1), anchored at
the exact zeros s=0 (x=1) and s=1 (x=2). Extracting `P(s)=Excel(1+s)/(s(s−1))`
and fitting a polynomial: residual falls monotonically with degree (deg4
4.7e-5 → deg12 1.8e-11), and the recovered coefficients MATCH the true-lgamma
expansion — **P(0) = 0.57721566… = γ (Euler–Mascheroni)** to 6.7e-16, P(1)≈
−0.2452512, etc. So Excel's (1,2) core is an accurate series-form approximation
`s(s−1)·P(s)` (NOT an arbitrary minimax rational); the ±5 ULP vs true is the
double-precision Horner evaluation of the degree-high P, not coefficient error.
This is the recoverable form. Note P(0)=γ means the earlier "recovered constant
γ is a true-function value not a fingerprint" caveat is resolved: γ IS the
leading coefficient of the (1,2) core.

## 2026-07-12 recovery attempts on the (1,2) core — the hard wall confirmed

With the `s(s−1)·P(s)` form and 249 dense (1,2) points, three recovery routes
were tried and all fail bit-exact — the core is a genuine custom high-order
approximation, not directly recoverable from ±5-ULP-rounded evaluations:
- **Truncated true Taylor** of P(s): catastrophic (1e14 ULP) — P's Taylor around
  0 converges only slowly toward s=1 (boundary singularity of the numerator's
  series), so Excel is NOT a Taylor truncation.
- **Recurrence** `lgamma(x)=lgamma(x−1)+log(x−1)` for (2,3): RULED OUT — residual
  drifts +5..+9 ULP (would be ~±1 if real), and band error SHRINKS with x
  ((3,4) ±1 vs (1,2) ±5) whereas recurrence would accumulate error. Each region
  has its own direct approximation.
- **High-precision polynomial fit** (mpmath, monomial in s): converges but slowly
  — D=16 still 47666 ULP off (D=15 → 207922). **Rational P/Q fit** (m,m): worse /
  ill-conditioned (≥6e12 ULP). Neither a modest polynomial nor a modest rational
  matches; the exact stored coefficients are not recoverable by direct fitting to
  the rounded data.

**Assessment:** the (1,2) core is the evidence doc's "custom Microsoft
implementation, no public source" — recovering it bit-exact needs (a) much denser
adjacent-double probes to tighten per-coefficient constraints, (b) the exact
evaluation ansatz (variable/center/staging), and (c) LLL/PSLQ against that ansatz,
or a match to an obscure historical lgamma. This is a dedicated multi-session
sub-campaign; deferred. Form + these negatives are the load-bearing progress.

## 2026-07-12 recovery harness + workflow — monomial plateau, form is structural

Built the recovery harness `smart-fuzzer/work/w109/G3-02-gamma/lgamma_recover.py`
(load dense band, high-precision fit of `R` in `lgamma(x)=(x-1)(x-2)·R(x)`, staged
double evaluation, bit-exact scoring, per-coordinate ULP refine, PSLQ constant-id).
Harvested a dense (1,2) constraint set (`answers-g12dense.json`, 1468 points: fine
0.0008 grid + adjacent-double clusters at 7 anchors).

Findings on the monomial ansatz:
- Best staging is `(x-1)·((x-2)·R)`, center 1.5, and it converges with degree
  (D16 27/1468 worst 4377 → D20 **564/1468 worst 54** → D22 571 → then conditioning
  noise). A scaled/Chebyshev-conditioned fit (u=(x-c)/0.5) is needed past D16.
- **PLATEAUS at ~571-578/1468 (~39%)**; the per-coordinate ±ULP refine only reaches
  578 — so the residual is **structural, not coefficient rounding**. The monomial
  `(x-1)(x-2)·Horner(R)` captures the function shape but is NOT Excel's exact
  evaluation structure.

A recovery workflow (6 parallel ansatz families: rational N/D, Cody sub-band split
at 1.5, compensated/double-double + Estrin evaluation, PSLQ-anchored coefficients,
exact published Cephes/fdlibm/Boost branches, alternative variable/no-factor) is
running with adversarial held-out verification of any family that beats the plateau.

## 2026-07-12 recovery workflow — 6 families, convergent hard wall + family ID

A 6-agent recovery workflow (rational, Cody sub-band split, compensated/dd eval,
PSLQ-anchor, exact published impls, alt-variable) with adversarial verification.
**None close** (best 601/1468 ≈ 41%), but they CONVERGED on the cause:

- **Precision monotonically HURTS** (compensated-eval): plain double 571 →
  double-double 460 → x87-extended-throughout 462. Falsifies extended-precision;
  Excel uses plain-double sloppy per-op rounding. `R=excel/((x-1)(x-2))` is
  provably NOT a polynomial (fit residual flat ~2.3 ULP, degree 20→32).
- **Exact-real ceiling of ANY smooth form ≈ 478/1468 — BELOW sloppy-double 571**
  (rational). So Excel's bits encode a specific finite-precision OP-FINGERPRINT,
  not a cleaner function. x87 per-op double-rounded (spill) poly reaches 579 —
  slightly better than plain, still a plateau.
- **FAMILY IDENTIFIED (published-impls):** fdlibm `__ieee754_lgamma_r` `1≤x<2`
  branch (centered at the lgamma minimum `tc=1.46163214496836224576`, 3-way
  parallel poly `p=z·p1−(tt−w·(p2+y·p3))`, `val=tf+p`) lands **within 5 ULP at
  EVERY point**; Boost `lgamma_small_imp<64>` `(x-1)(x-2)(Y+P/Q)` within 6.
  Excel is a minimax rational in THIS family. But refitting Excel's coefficients
  into fdlibm's exact op-tree still caps ~225/750 with a stubborn 4-ULP residual
  that ULP-refine cannot remove.
- A **universal ~5-ULP wall** appears in every form/cut/precision → the residual
  is Excel's **exact per-operation evaluation graph** (op-order + per-op rounding),
  NOT the coefficients, function form, variable, or subbanding.

**Verdict:** GAMMALN(1,2) is the "custom Microsoft implementation" — a minimax
rational in the fdlibm/Boost family, reproducible only by matching Excel's exact
internal op-graph. Not recoverable from observed bits by form/coefficient fitting.
Hardest lane in W109; DEFERRED. The one untested experiment for cycle-back: take
fdlibm's tc-centered op-tree structure EXACTLY and apply the x87 per-op double-round
(spill) model while jointly refitting coefficients — the only precision×op-graph
combination the workflow did not isolate. Harness: `lgamma_recover.py`;
data: `answers-g12dense.json` (1468 pts). NB: `identify_constant` tol was 1e-25
(can't fire on doubles) — widen to ~1e-15 if PSLQ-anchoring is retried.

## 2026-07-12 tree-aware probing — TREE largely identified, op-graph is the floor

Following the 1990s-x87 + Gaussian-quadrature-probing insight: instead of blind
fitting, probe at exactly-representable offsets and read the tree directly.

**Findings (the tree is now substantially pinned):**
- **(b) x87 on fdlibm's tc-tree does NOT help**: fdlibm's exact tc-branch scores
  177/750 under the realistic x87 model (80-bit within expressions, round at each
  `double` temp) vs 179/750 plain — same worst-5. Excel's tree ≠ fdlibm's tree.
- **Exact-offset peel** `x = 1 + m·2⁻ᵏ` (so x−1 is an exact power of two): the value
  peels term-by-term. `excel(1+2⁻ᵏ)/2⁻ᵏ → −0.5772156649015329` to ~52 bits ⇒
  **D₁ = correctly-rounded −γ** (digamma(1)); Excel near x=1 tracks the TRUE function
  to ~1 ULP.
- **Breakpoint at x=1.5** (Cody's classic split): the window-median error flips sign
  — `+1/+2` ULP on [1.1,1.5], zero at 1.5, `−1/−2` on [1.55,2] — the fingerprint of
  two separate minimax approximations meeting at 1.5 (rational in x−1 below, x−2 above).
- **Cody form `lgamma(x)=(x−1)·[(x−1)·N/D + D₁]`, D₁=−γ, refit N/D on [1,1.5]**: best
  229/718 at (5,5), worst 15. Still a plateau.

**Why every form plateaus (~32–41%):** fitting to ±5-ULP-rounded output cannot recover
coefficients to better than ~5 ULP (fdlibm's PUBLISHED coeffs give worst-5 everywhere;
any REFIT from Excel's rounded bits gives worst≥5-15). So the residual is the rounding
floor of the fit itself. Closing it needs Excel's EXACT stored coefficients + exact
op-order — information not present in the output bits. LLL can't break the floor because
setting up the lattice requires the exact op-graph, which is the unknown.

**Tree now known:** fdlibm/Cody-family minimax rational, split at 1.5, D₁=−γ, near-1 ≈
true function. **Unknown (the wall):** the exact N/D coefficients + per-op evaluation graph
on each half. Realistic closure paths: (1) obtain Excel/MS's actual lgamma source constants;
(2) a joint op-graph × coefficient search far larger than fitting. DEFERRED — best-characterized
hard lane in W109.

## 2026-07-12 residual-DRIVEN recovery (replaces pass/fail scoring)

Pass/fail match-count is a near-flat, information-destroying objective for this
inverse problem. Replaced it with a **residual-structure** harness
(`residual_harness.py`, `gn_fit.py`, `opgraph_scan.py`): the signed ULP residual
`Excel(x)−eval(c,x)` is decomposed into a SMOOTH component (moving-average →
coefficient/metric/form error) and a HIGH-FREQUENCY component (→ op-graph /
per-op rounding). This separates the two unknowns and gives each a continuous
objective.

Findings on [1,1.5] (netlib Cody form, 718 pts):
- **Coefficients are recoverable to ~1 ULP.** Gauss-Newton on the residual (value
  space, numerical Jacobian) drives the SMOOTH component `1.32 → 0.99 ULP`
  (exact 180 → 224) — the coefficient error is small and shrinks under GN, i.e.
  Cody's coefficients are already within ~1–2 ULP of Excel's.
- **The op-graph family is x87-extended.** The NOISE floor is op-graph-specific
  and coefficient-independent. Ranked over 9 stagings: every **x87** variant
  (1.24–1.29 ULP) beats every **plain-double** variant (1.41–1.58); `x87
  continuous` (extended registers, single final round) is whitest at **1.24**.
  This is a robust structural identification — Excel evaluates the rational in
  x87 extended precision (consistent with the 1990s x87 origin), which the
  pass/fail count (all ~25–40%) completely hid.
- Neither the smooth (~1.0) nor the noise (~1.24) floor is yet 0, so the EXACT
  x87 staging + joint coefficient optimum are not both pinned. The residual
  floor is now the objective to minimize.

**Reformulated recovery pipeline (residual-driven):** (1) enumerate op-graph
stagings, rank by NOISE floor → pin the x87 staging that whitens it to ~0;
(2) joint/stable Gauss-Newton in that op-graph to drive SMOOTH → 0; (3) LLL /
`fpminimax` for the last bit. The blocker to full closure is a numerically stable
x87-op-graph Gauss-Newton (the current x87 Jacobian is noisy through the rounding)
plus finer staging enumeration. Artifacts in `smart-fuzzer/work/w109/G3-02-gamma/`.

## Next steps (Phase-5b)

1. **Pin the Stirling boundary** by live bisection in (10.25, 11.0].
2. **Identify the internal CRT log** from the 3 residual Stirling rows +
   targeted probes: for x ≥ 11 the result is `(x-0.5)*log(x)+…`, so each
   GAMMALN answer brackets `log(x)` to sub-ULP; harvest a few hundred
   bracketing constraints and race UCRT-log revisions / SSE2 minimax
   variants against them.
3. **Recover the custom small-x kernel**:
   a. Map band edges: dense ULP-error-vs-true curve; edges appear as
      error-curve discontinuities; bisect each edge to the exact double.
   b. Within each band, hypothesize `prefix(x) * (Y + P(t)/Q(t))` forms
      (anchored at the exact zeros) and recover coefficients by integer
      relation / LLL on high-density answer bits (the racer gets a
      `fit-rational` mode).
4. Only after 1–3: promote `gammaln` kernel, compose GAMMA (+ reflection
   via identified excel_sin for negatives), COMBIN, then re-race G3-01.

Working artifacts: `check_gammaln_split.rs`, `check_gammaln_recur.rs`,
`check_gammaln_fdlibm.rs`, `check_gamma_cephes.rs` (racer bins);
`band_matrix.py`, `boost_small.py` (work dir).

## Session-6 breakthrough (2026-07-18, agent L): the (0,11) core is Cody & Hillstrom DLGAMA with RE-FIT coefficients

Sanity gate reproduced (136/139 Stirling, same 3 documented misses). New
zero-capture structural identification of the core from existing corpora:

- **Downward recurrence identity** excel(x) == double(excel(x+1) - log(x))
  is bit-exact 32/32 for all pairs x <= 0.62 and fails from 0.70 up
  (catastrophic +55,418 ULP at 0.99999 proves direct evaluation there). This
  is EXACTLY Cody's DLGAMA control flow below PNT68 = 0.6796875 (reuses the
  direct-band rationals with CORR = -log(x)). Threshold bracketed (0.62,
  0.70], PNT68 the strong prior.
- **GAMMALN(4) = CR(ln 6) EXACTLY** (while GAMMALN(3) = CR(ln 2)+1): the
  fingerprint of Cody band-4 RES = D4 + (x-4)*(XNUM/XDEN) publishing the
  stored anchor verbatim. D1 = -gamma was already peel-recovered.
- Full skeleton consistent with all data: [eps?,0.5] P1(XM=x, -log) |
  (0.5,PNT68) P2(XM=x-1, -log) | [PNT68,1.5) P1(XM=x-1) | [1.5,4) P2(XM=x-2)
  | [4,~11) D4-form | >=11 Cephes Stirling. Edge detector: no other jumps.
- **Coefficients are a Microsoft RE-FIT, not any published set**: published
  Cody scores b4 231/385 (worst 3, x87-continuous objective); +-1..3-ULP
  per-coefficient hill-climb stalls (+4 rows) — the decimal-conversion-error
  hypothesis is FALSIFIED; Gauss-Newton reaches b2 450/1247 / b4 238/385
  worst 2 on a FLAT equivalent-fit manifold (genuine re-fit).
- b4 miss profile grows toward x=10: consistent with a re-fit on [4,11]
  (Stirling switch moved from Cody's 12 to ~11). Remez-on-[4,11] test
  designed as follow-up.
- PSLQ negative on fitted doubles (expected for minimax output).
- Best composite forward model now: published-Cody core (x87-continuous) +
  Cephes Stirling >= 11: 1096/2850 = 38.5% exact, worst 6 ULP.

Batteries designed (capture queued): batch-L-boundary.json (1,793: Stirling
switch pinning incl. >=-vs-> and derived-quantity discrimination),
batch-L-core.json (9,642: threshold ladders with recurrence partners,
EPS-branch ladder, multi-scale peel ladders at anchors 1/2/4, adjacent-double
clusters to break the GN manifold, dense miss-zone fills, golden-ratio
held-out sweep).

EXTERNAL-SOURCE NEED (manual access; automated fetch bot-blocked): Cody &
Hillstrom 1967, Math. Comp. 21(98):198-203 — per-interval coefficient tables
at MULTIPLE precision levels; Excel may use a different table entry or a
FUNPACK-era set. Control: netlib SPECFUN algama.

## Round-2 recovery (2026-07-18, agent L) — skeleton nearly pinned; [8,12) is the one unidentified segment

- **Stirling switch**: the (10.25,11] bracket was an artifact (rational and
  Stirling CONVERGE below the switch — the match ramps 0% at 10.0 -> 84% at
  11.0 -> 100% by 11.44 with no flip). Real bracket (11.43, 12.75); at 12.75
  the rational family is dead (-186 ULP) while Cephes-Stirling is +1. Prime
  candidate: Cody's TWELVE = 12.0. Round-3 sw12 block pins it.
- **Low-branch threshold is a literal 0.7 compare, NOT PNT68**: recurrence
  identity exact through 0.6953125, first direct row at double(0.7); rpair
  census 367/367 exact on (0.02,0.5). **No -log(x) EPS early-out** (identity
  runs bit-exactly to 2^-57). Gap (0.6953125,0.7) pinned in round 3.
- **Band-4 = TWO regimes, seam at 8.0**: [4,8) near-closure (GN 75.6% exact,
  worst 1, x87c); [8,10.25) walls at rms 0.89 for EVERY rational of the
  family (recentering-invariant; upward recurrence ruled out; a
  Stirling-refit-tail blend improves [8,11.5) to 70.6% but degrades >=11.5)
  — a two-regime blend signature. SUPERSEDES the [4,11]-Remez hypothesis.
  [8,~12) is now the single unidentified segment (best ~38-51%, worst 3).
- **Cody & Hillstrom 1967 verbatim RULED OUT** (n=7 race plateaus at
  38.8-44.7% like SPECFUN; n=6 accuracy class excluded, worst 27-668).
  Excel = the 1967 FORM SET (incl. -ln x + R1(x+1), the proven identity)
  with retuned thresholds (0.7; seam 8; switch ~12) and a THIRD,
  Microsoft-refit coefficient set at n=7 accuracy. GN real-curve residual
  differs from BOTH published sets by more than op-rounding (amp 2.7-5.9
  ULP, 10-12 sign changes) — no re-staging of published coefficients can
  close.
- **Banked coefficient fingerprint**: b4 r0 = N4(0)/D4(0) sits rel -3.34e-15
  below Cody's published ratio (20x stability margin).
- Peel-read method correction: deg-3 anchor reads were truncation-biased;
  deg-8 double-window reads land at the 5e-14/9e-13 rel read floor.
- **Held-out promotion (golden-ratio sweep, never fitted): composite best
  model 644/1199 = 53.7% exact, worst 4** ([4,8) 70.7% worst 1; [8,10.25)
  38.5%; b1 52.1%; b2 46.1%; x>=11.44 Cephes-Stirling).
- Round-3 battery captured: 2,795 probes (gap/sw12/seam8/slope/expo/held2).

Note on the n=7 validation: the main-session high-precision check (E =
1625.2/1703.7/1606.1) and agent L's double-rounded-coefficient check (1596/
1654/1582) are BOTH correct — the delta is coefficient double-quantization,
below the n=7 approximation error. No OCR repairs were needed anywhere.

## Round-3 final pinning (2026-07-18, agent L) — GAMMALN structurally CLOSED except b1/b2 coefficients

- **Low-branch threshold PINNED**: recurrence-exact through 0x3fe6666666666665,
  first direct row at 0x3fe6666666666666 = double(0.7) — clean single flip at
  adjacent-double resolution. Predicate: x < 0.7 (literal C double) selects
  -log(x) + core(x+1); x >= 0.7 direct. The 0.5 "sub-split" is just band
  dispatch at x+1 (no constant of its own).
- **THERE IS NO STIRLING SWITCH AT 12 — x >= 8 is ONE formula, IDENTIFIED**:
    q = (x - 0.5)*log(x) - x + 0.91893853320467274178   (plain double, L-to-R)
    z = 1/x; y = z*z
    w = w1 + y*(w2 + y*(w3 + y*(w4 + y*(w5 + y*w6))))   (fdlibm e_lgamma_r
        w1..w6 VERBATIM)
    res = q + z*w
  **5739/5749 = 99.83% bit-exact over x in [8, 1030], worst 2.** Plain double
  (x87 degrades to ~52%); fdlibm's own (x-0.5)*(t-1)+w0 staging scores 46.8%
  — Excel reuses fdlibm's coefficient VECTOR in a DIFFERENT staging. The old
  "Cephes A5 / switch in (10.25,11]" verdict is SUPERSEDED (A5-vs-w agreement
  artifact). Of 10 residual rows: 7 = internal-CRT-log +-1 (separate lane),
  3 unresolved (0.05%).
- **x=8 seam pinned**: rational for x < 8, Stirling for x >= 8 (8-2^-k on the
  rational for all k to 2^-44; 8.0 itself on Stirling; excel(8)=CR-1 computed
  not anchored). The [8,12) "wall" is CLOSED — it was this formula all along.
- **[4,8) IDENTIFIED as published SPECFUN P4/Q4 under x87-continuous
  evaluation: 76.3% worst 1** (GN adds nothing) — only the exact +-1 spill
  pattern remains open.
- **Composite promotion (held2, never fitted): 314/400 = 78.5% exact, worst 4**
  (composed 81% w1 | b1 28% w4 | b2 55% w3 | [4,8) 79.1% w1 | x>=8 99.3% w2).
  vs PRODUCTION (Lanczos log-domain): 0/79 exact, errors to 1370 ULP —
  LANDING JUSTIFIED. b1 [0.7,1.5) flagged provisional per the held-out rule
  (gn2 degraded 48%->28% held); b1/b2 exact coefficients remain the one open
  identification (published sets + 1967 verbatim all ruled out; anchors
  D1=-gamma, D2=1-gamma CR pinned).
- Landing spec + b1/b2 provisional-coefficient decision requested (in flight).

## Lane 4 (2026-07-18, agent-S + fresh gate) — B2 re-identified CONTINUOUS and re-landed; B1 confirmed at its wall

Agent-S ran the staging×coefficient co-search on the round-3-pinned forms
(clean fit split — it also found agentL's gn2 fit had been mildly
held2-CONTAMINATED: `fit_sets()` excluded only `held-`). Deliverables:
`agentS_results.md` + `agentS_*.py/json` in the G3-02 work dir.

**B2 [1.5,4.0): the op-graph is FULLY-CONTINUOUS x87 (`e/e/e`, one final
round) — the same class as B4 — not the spill model previously landed.**
Held-blind noise floor 1.077 (continuous) vs 1.113 (spill), robust under
each staging's own refit coefficients. The selection drama is a method
exemplar: a spill-staged polish EXISTED that passed the formal held2 gate
(317>316) but its seed/staging choice had touched held-out; the fresh
never-probed b32 corpus (1,600 rows) ruled: that candidate 505/1,200 —
WORSE than the landing 518 (selection leakage, exactly the MINVERSE
lesson) — while the held-blind pick (LM refit under continuous) won at
**549/1,200 (45.8% vs 43.2%)**. LANDED: gammaln.rs B2 now continuous with
the LM coefficients (suite green; port bit-matches the reference on b32).
Aggregate across all 1,554 banked+fresh b2 rows: 711 vs 686.

**B1 [0.7,1.5): confirmed at its form-family wall.** Every refit overfits
(held-out drops); the published 1967 n=7 plain-double stands. Fresh b32:
123/400 (30.8%), consistent. Structure: only ~36% of misses are within 1
ULP pre-round; real distances reach −3.4 ULP — outside ANY coefficient
choice in the enumerated staging family. CVP method caveat banked: the
pre-round distance MUST be computed at mp.prec≈200 (dps-15 cancels
catastrophically and fakes integer-clustering).

**Open (wall 5 refined):** B1 op-graph (and B2's residual ~54%) are outside
the (num,den,div,outer,assoc,fma,recip)×(d,s,e) family. Agent-S's designed
next probes: (i) two-step argument reductions ((x−1)−1, (x−0.5)−0.5);
(ii) non-minimax coefficient family (Remez under a different weight — the
~1-ULP irreducible coefficient error hints Excel's table isn't a plain
minimax); (iii) independent outer 2-op spill mask re-run AFTER an e/e/e
refit. See W109_WALL_CLUES_LEDGER.md.
