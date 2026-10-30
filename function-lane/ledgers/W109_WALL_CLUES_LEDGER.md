# W109 wall-clues ledger

A running trail of clues and instruments for the parked op-graph walls,
collected en route through other lanes (started 2026-07-18, four-lane sweep).
Read together with W109_CAMPAIGN_RESUME_20260718.md (wall definitions and
designed probes). Add to this file whenever a lane surfaces something a wall
will want; date every entry.

## Wall 1 — chain-microdetail ±1 (series r / exp idealization class)

- **2026-07-18 (lane 1):** two fresh banked class members, both on the plain
  exp path (no series involvement):
  - `b24W-b2-0340`: WEIBULL cdf, x bits `4018222d34979553` (x≈6.03338,
    α=2, β=2, t≈9.10041): Excel's internal `exp(−9.10040519235115…)` is
    **+1 ULP above our chain** (published cdf 1 below all staging
    candidates). Args and expected bits in `answers-b24-weibull.json`.
  - `b28-3838`: WEIBULL cdf, args x=`3fc3d9d7eab87363` α=`401dd48b49e40d40`
    β=`3fd1feab7fc34ab8` (t≈0.0117): production −2 ULP. Only miss in 6,000.
  - Class rate stays ~0.01–0.02% across every corpus (1/17,300 b24-weibull;
    1/6,000 b28; 3/30k POISSON; 4/18k expm1). The rows are argument-stable
    (deterministic), scattered, and NOT correlated with the F2XM1 fraction
    bins we binned earlier — worth re-binning against the reduction
    residue `f = t·log2e − round(t·log2e)` with the new rows added.
- **Instrument:** `x87_serve` op server + `x87client.py` (lane 1) makes
  op-by-op chain dissection scriptable from Python — apply to agentQ_diag7's
  seven rows without hand-built Rust harnesses.

## Wall 2 — ln-amplification at a≥3 (GAMMA.DIST series)

- **2026-07-18 (lane 1):** WEIBULL/EXPON proved the closed-form bodies form
  their products as **x87 double-rounded ops** (RN64 then RN53 spill). The
  b26 a·L staging race assumed a plain product; a DR product `RN53(RN64(a·L))`
  is a one-line re-race on the banked b26 rows (x87client makes this
  minutes). If the gamma series body is (even partially) the legacy x87
  class, the a-growth of the worst-case (4→7→10) could be DR-accumulation,
  not L-delivery.
- Caveat the other way: GRATIO itself was proven plain-SSE2 by structure
  racing — the two body classes COEXIST in the 2010 rewrite (lane-1 big
  picture). Which class owns the `t1 = a·L − y` site is now a live question
  rather than settled background.

## Wall 3 — erf 190-path (C10r plateau, 2^Ez grid source)

- **2026-07-18 (lane 7): b33 CROSSING SWEEP — the wall resolves into
  per-window integer-ULP term corrections.** Whole windows land bit-exact
  under a single term nudge (A1w1 `M+1` 60/60; A2w1 `b1+1` 58/60; A3w2
  `M−2` 56/60): every window has a CONSTANT argument offset of
  ±(1–4)·2⁻⁵³. Same-anchor consistency separates lf-side (A1: both
  windows −1·2⁻⁵³) from bd0-side (A3/A4: p-varying) realizations; the
  chain is exonerated with POSITIVE evidence (staircases reproduce exactly
  under one correction). stirlerr is inert (ulps ~2⁻⁶² — below
  resolution). **Endgame = integer-ULP linear system**: ~10 short windows
  per anchor overdetermine the per-class term corrections; then match the
  solved values against published bd0/lf realizations. Template:
  `lane7_b33*.py` + answers-b33. Slow-walk windows need near-mode p
  (design note: ulps/step ran 3–1,066, target 5–50).
- **2026-07-18 (lane 6d): EXACT-CONSTRAINT REFRAME (user directive) — the
  wall's information budget stated precisely.** Single reads carry no
  information below publication granularity (decode floor ≡ output
  granularity in argument space); match-rate deltas in the 32–36% band
  were phase, not signal. Pair search RUN AND RETIRED BY ARITHMETIC
  (zero pairs ≤64 ulp64 in b29; the p-dial is 2^8 too coarse to design
  collisions). **The right instrument is the b33 boundary-crossing sweep**
  (erf tooth-law bisection with a KNOWN argument model — first time both
  sides of the equation are available): p-ulp sweeps for fixed (k,n),
  each published-staircase transition = one exact inequality pinning
  CHAIN(arg) to a known boundary within one p-step; anchors spanning
  |arg| 10–600 separate argument-side (low |arg|) from chain-side
  (high |arg|) deviations. Full design in the lane-6d note section —
  execute as the next session's opening move.
- **2026-07-18 (lane 6c): joint solve — flagship hypotheses refuted;
  status sharpened.** x²-spill (erf), M-as-tbyte and every lf composition
  (BINOM), and the c-vs-reduction-fraction chain-error map (all-rows) are
  ALL refuted. With the argument families CLOSED (lc/lf doubles + exact
  subtract), the residual ±1 publication scatter is chain/publication-side
  — but note the epistemic correction: windowed-76% was weak evidence
  (any monotone chain windows); the true discriminators are the no-window
  classes (confirmed = visible-level term classes) and correction-map
  structure on ARGUMENT-CERTAIN rows. Next: (i) c(f) map on
  argument-certain subsets of BOTH corpora (same map ⇒ chain-side);
  (ii) cross-corpus exact-argument pairs (<1 ulp64 apart) — their
  published values must agree under ANY deterministic chain, the cleanest
  litmus; (iii) ±300 narrow-interval solve with joint term nudges.
- **2026-07-18 (lane 6b): MERGE CONFIRMED — walls 3 and the BINOM blocker
  are ONE.** The erf j-scan (`check_erf190 <dir> jscan`, dev corpus only,
  b9heldout untouched) reproduces the BINOM signature number-for-number:
  windowed 76.5% (BINOM 76%), no-window 23.5% (= the j-pipeline park-phase
  visible class), centers median-0 with ±240-ulp64 sub-double scatter.
  The unified wall: **sub-double argument composition at extended-entry
  exp sites** (how 32-bit codegen forms `a·ln_ext(x)` / `lc − 0.5·lf` at
  64-bit before the chain) + a per-site ~24% visible-level term class.
  One unknown, two corpora, one instrument (the narrow-interval solver).
- **2026-07-18 (lane 6): THE CHAIN IS EXONERATED — the wall is
  ARGUMENT-SIDE.** The j-interval scan on the b29 oracle pairs proves the
  composed extended-entry fFEXP chain reproduces Excel bit-for-bit given
  the right 64-bit argument (consistent interval for 76% of rows; the rest
  are known ±1-term rows). What is unknown is the argument's sub-double
  content (below the decode floor): single-source lf hypotheses all
  rejected by the narrow-interval solver; a second source correlates with
  EXTREME p. **Re-read the erf C10r plateau as argument-delivery detail,
  not chain realization — run the same j-scan on b9heldout with C10r's
  argument model to confirm the merge.** Method: `lane6_jscan/solver.py`
  (the narrow-interval solver is the reusable instrument); server ops
  `lnext` (hardware extended fyl2x as hi+lo) + `cexpext2`.
- **2026-07-18 (lane 5): THE WALL GAINED A DIRECT ORACLE.** BINOM's
  dbinom_raw argument staging is now identified to publication-noise level
  (82.5% of decodable b29 rows at d≈0.00), and the end-to-end blocker is
  the SAME primitive as this wall: the fFEXP chain entered with an
  EXTENDED argument. The ~500 correct-argument b29 rows are
  (arg_ext64, published_bits) pairs — attack the extended-entry chain
  realization on THESE (argument exactly known!) instead of erf's
  never-recovered arguments. Tooling: `cexpext2 hi lo` server op runs the
  current composed chain from an exact 64-bit argument; it agrees with
  Excel only ~45% on correct-arg rows — enumerate reduction/publication
  micro-variants (f2xm1 argument handling, rndint mode, store order)
  against these pairs. A win here closes BOTH the erf plateau AND BINOM
  (and presumably NEGBINOM + the POISSON small-λ side).

- **2026-07-18 (lane 1):** no direct new probe, but two transferable facts:
  (i) association ORDER is recoverable and matters — the WEIBULL pdf race
  was stuck at 805/1200 until the tree enumeration found division-first;
  the erf polynomial-evaluation candidates were enumerated over staging
  variants but (check the agentJ ledger) possibly not over association
  orders of the rational's numerator/denominator combine.
  (ii) mixed spill masks (some intermediates extended, some spilled) are
  REAL in this codebase — round-6 style tree×mask enumeration via mpmath
  is cheap and exhaustive; the erf chain-floor question ("parked vs
  register-continuous") is exactly a mask question.
- b9heldout (256 rows) remains the reserved unraced promotion gate.
- **2026-08-30 (ERFC F-body firehorse):** the 96h store-mask campaign
  exhausted all six R1m 26-bit PQR+t cubes (402,653,184 configs) on the
  NSWC mid_cut=1.5 bar graph. Ceiling moved **3332 → 3336 / 7741**, still
  max 7 ULP, still 0 pin hits. Extra R-Horner spills (`mask=0x0048000`)
  are a +4-row wiggle, not the body. Constraint: missing per-stage stores
  on published NSWC DERFC0 are not the identity.
- **2026-08-31:** `R1/z0/r0` finished unchanged. R4 (AA/BB 19-bit, all
  six axes), R2 (Cody 16-bit, all six), and R0aabb (AA/BB/E ±1 ULP, best
  2924/7741) added **zero** leaders. NSWC/Cody store-site and last-bit
  are exhausted. Next object is F itself via implied `Q/excel_exp(−z²)`.
- **2026-08-31 implied-F packets:** Cephes erfce, fdlibm F, NSWC CC/DD,
  A&S 7.1.14 CF, Gautschi CF. None is the body. NSWC still leads mid
  (2388/7741 max 7). CF A&S leads tail exact (1283/5934) with the same
  189 ULP ceiling. fdlibm split-exp F ≈ libm on tail (wrong staging).
- **2026-08-31 F_or w-oracle:** `excel_exp(-RN53(RN64(z·z)))` vs native
  `z*z` changes 3/13687 implied-F values (max 190 ULP, tail). Pins
  identical. Split `excel_exp(-z)*excel_exp(-z)` is dead. The 7 ULP mid
  ceiling is an F-form object, not a missing square-store.
- **2026-08-31 residual hist:** 2389 exact + 3414 at 1 ULP on mid NSWC
  (75% ≤1 ULP); one row at 7 ULP. Oscillatory comb (2142 sign switches).
  Piecewise NSWC/CF at 1.6 → 3699 exact. CF tail saturates at n=21.
  Next: CF x87 store-mask campaign on firehorse.
- **2026-08-31 residual cluster + complementary Lentz:** the lone mid 7-ULP
  row is `z=1.1842387490730035` (the G-F3 direct/implied conflict z).
  Residual sign flips across the published NSWC x=2 cut (PQR high, AA/BB
  low). ULP≥4 clusters in `[0.77,1.06]`. Sweep: the 7-ULP row is implied-Q
  (`direct=0`); direct ERFC.PRECISE mid max is 4 ULP. x87 NSWC F with PQR
  cut 1.5 / AABB to 4 is the new constraint (**2939**/7741 mid, 4182
  all-exact), not an identity. CF `n*` is spread, not a truncation law.
  Firehorse: backward-CF store-masks (12 vCPU) plus even-odd/Lentz C/D
  store-masks (4 vCPU). No more NSWC PQR 26-bit cubes.
- **2026-09-01 compose:** x87 A&S CF (backward or even-odd) is +5 tail vs
  native at the n=24 plateau (1288). Extra exacts are implied-Q only.
  Best constraint: x87 NSWC PQR@1.5/AABB@4 on mid (2939) plus x87 CCDD
  until 6.2 then x87 even-odd on tail (1298) → **4237** all-exact. Not an
  identity; pins still inexact. x87 CCDD-alone loses to native CCDD.
- **2026-09-01 sites:** on that mid graph, every 1-ULP leftover is
  `nextafter` of F. PQR named-site cube best is mask 0; AABB +3; R-step
  +5. Direct pin z=2.125 still 4 ULP. Do not spend more named-store bits
  on this graph.
- **2026-09-01 leftover packets:** 941 x87-cut misses are native-NSWC
  exact (rounding trade, union 3880/7741). 2164 leftover have no named
  exact. t-formula does not hit leftover PQR. `CF/gaut/n12b2` cube
  finished with no leader move.
- **2026-09-01 selector:** native-vs-x87 PQR union 1803/3475 is not a z/t
  LSB or z-cut rule; always-x87 (1318) beats every cheap predicate.
  AABB neither still 2304/4266. Do not land a per-row rounding pick.
- **2026-09-01 direct leftover:** merged leftover is implied-Q. Direct mid
  misses vs x87-cut are 144 rows, max 4 ULP; 63 have no named exact.
  Pin z=2.125 is one of two 4-ULP direct rows. The 7-ULP merged ceiling
  is not an ERFC.PRECISE wall.
- **2026-09-01 direct Cody x87:** 85/226 mid, +3 over x87-NSWC, pins still
  inexact. `CF/as714/n12b2` cube finished with no HIT.
- **2026-09-01 AABB E0 ±1:** E0−1 improves pins 2.125/1.875 but loses 25
  direct mid exacts. 3.75 ±1 is the same trade. n20/n21 CF cubes finished
  on the named x87 plateau; no HIT.
- **2026-09-01 MATH77 F_or:** Chebyshev F leads named tail (1437/5946) and
  all-exact (4260), still not an identity. Mid still x87-NSWC (2939).
  n21 cube done; n24 Gautschi in progress at named-plateau chunk_best.
- **2026-09-01 MATH77 F correction:** the 1437/4260 scores used MATH77 Q
  over `w_rn53` (mixed exp). True F=`derfc1/y` is mid 2665 tail 1261, behind
  x87 NSWC mid and x87 CF tail. Retract the Chebyshev-leader claim.
- **2026-09-01 firehorse cube gate:** `CF/gaut/n12b2` finished 2^24 with
  no new HIT. Leaders still R0 piecewise (mid 2416 `piece/cut=1.6`, tail
  1294 `piece/cut=5.6`). Region now `CF/as714/n12b2` (~20%). Lentz still
  `evenodd/as714/n12b2` (~22%), HIT_TAIL 1288 at mask=0. Constraint, not
  an identity. Snapshots in `w109-erfc-fbody-campaign/` and
  `w109-erfc-lentz-campaign/`.
- **2026-09-01 firehorse cube gate 2:** also finished `CF/as714/n12b2`,
  `CF/gaut/n16`, `CF/as714/n16`, `CF/gaut/n20`. No new HIT; leaders still
  2416/1294. Region now `CF/as714/n20` (~71%). Lentz still
  `evenodd/as714/n12b2` (~43%), HIT_TAIL 1288 at mask=0.
- **2026-09-01 firehorse cube gate 3:** finished `CF/as714/n20` and
  `CF/gaut/n21`. No new HIT; leaders still 2416/1294. Region now
  `CF/as714/n21` (~83%). Lentz still `evenodd/as714/n12b2` (~49%),
  HIT_TAIL 1288 at mask=0. Next fbody cubes are the two n24 2^24 stores.
- **2026-09-01 firehorse cube gate 4:** finished `CF/as714/n21`. No new
  HIT; leaders still 2416/1294. Region now `CF/gaut/n24` (~22%). Lentz
  still `evenodd/as714/n12b2` (~56%), HIT_TAIL 1288 at mask=0. Remaining
  fbody: `CF/gaut/n24` then `CF/as714/n24`.
- **2026-09-02 firehorse cube gate 5:** finished `CF/gaut/n24`. No new
  HIT; leaders still 2416/1294. Region now `CF/as714/n24` (~16%). Lentz
  still `evenodd/as714/n12b2` (~84%), HIT_TAIL 1288 at mask=0. Remaining
  fbody: `CF/as714/n24` (last cube).
- **2026-09-02 firehorse cube gate 6:** finished `evenodd/as714/n12b2`
  and `evenodd/as714/n16`. No new HIT; HIT_TAIL still 1288 at mask=0
  (nonempty even-odd stores did not beat named x87). Lentz now
  `lentz/gaut/n12b2` (~3%). fbody still `CF/as714/n24` (~75%).
- **2026-09-02 firehorse cube gate 7:** finished `CF/as714/n24`; all
  selected fbody CF cubes done (`exit-regions`). No new HIT; leaders
  still 2416/1294. Lentz still `lentz/gaut/n12b2` (~21%), HIT_TAIL 1288
  at mask=0. fbody not restarted (same launcher would re-exit).
- **2026-09-02 firehorse cube gate 8:** finished `lentz/gaut/n12b2`. No new
  HIT; HIT_TAIL still 1288 at mask=0 (nonempty Lentz gaut n=12 stores did
  not beat named x87 even-odd). Lentz now `mlentz/gaut/n12b2` (~9%), 12
  threads, 42.57/96h. fbody still `exit-regions`; not restarted (same
  launcher would re-exit).
- **2026-09-04 firehorse cube gate 9:** finished `mlentz/gaut/n12b2`. No new
  HIT; HIT_TAIL still 1288 at mask=0 (nonempty modified-Lentz gaut n=12
  stores did not beat named x87 even-odd). Lentz now `lentz/as714/n12b2`
  (~13%), 12 threads, 52.55/96h. fbody still `exit-regions`; not restarted
  (same launcher would re-exit).
- **2026-09-03 firehorse cube gate 10:** skipped duplicate `mlentz/as714/n12b2`;
  leftover n16 cubes finished with no HIT. `lentz/gaut/n21` then moved
  HIT_TAIL 1288 → 1298 (`mask=0002588`) → **1316** (`mask=0142180`). That
  21-bit cube is done. Lentz now `lentz/as714/n21` (~3%), 12 threads,
  62.59/96h, alive. Mid still 2389 `nswc_derfc0`. Constraint, not an
  identity; do not land. fbody still `exit-regions`; not restarted (same
  launcher would re-exit).
- **2026-09-03 firehorse cube gate 11:** packed n24 is live. Lentz now
  `lentz/gaut/n24` (~10% of 2^24, chunk `0x01a8000`), 12 threads,
  66.63/120h. HIT_TAIL still 1316 at mask `0142180`. chunk_best_tail=1239.
  Mid still 2389 `nswc_derfc0`. Constraint, not an identity; do not land.
  fbody still `exit-regions`; not restarted (same launcher would re-exit).

## Wall 4 — bgrat body op-graph

- **2026-07-18 (lane 1):** the falsified bgrat families were "53-bit per-op
  DR" and "register-resident" — but the WEIBULL pdf shows the actual bodies
  use **specific C-source association orders** (division first) under
  per-op DR, and that getting the ORDER wrong while the op class is right
  still costs ~25% of rows at ±1. Recommend: re-enumerate the bgrat body
  candidates as expression TREES (round-6 method, `lane1_pdf_round6.py` as
  the template) over the shared-z group-intersection corpus before
  declaring the family dead.
- If bgrat forms powers `x^a`/`(1−x)^b` anywhere via pow, the site is now
  known: `excel_pow_chain` (DR product, no shortcuts) — earlier races used
  idealized pow models at some stages.

## Wall 5 — GAMMALN b1/b2 coefficients

- **2026-07-18 (lane 4, agent-S + b32 fresh gate): B2 RE-LANDED as
  fully-continuous x87 with LM-refit coefficients** (fresh b32: 549 vs
  518 / 1,200; noise floor 1.077 vs 1.113; B2 and B4 are now the SAME
  op-graph class — architecturally coherent). B1 confirmed AT ITS WALL:
  published-1967 plain double is the held-out optimum of the entire
  (d,s,e,fma,recip)×association staging family; misses reach −3.4 ULP
  pre-round (not coefficient-fixable). What remains is outside the family:
  next probes = two-step argument reductions, non-minimax (re-weighted
  Remez) coefficient family, outer 2-op mask after e/e/e refit
  (agentS_results.md §7).
- Method clues banked: (i) CVP pre-round distances need mp.prec≈200 —
  dps-15 catastrophically cancels and fakes integer clustering; (ii) the
  gn2 fit was held2-contaminated (agentL fit_sets excluded only `held-`) —
  always exclude EVERY held set by prefix; (iii) the fresh-corpus rule
  worked exactly as designed: a formally-gate-passing candidate whose
  selection touched held-out LOST on never-probed rows (505 < 518).

## Wall — internal extended lgamma (G3-02)

- **2026-07-18 (lane 2): NEW MEASUREMENT WINDOW.** BINOM.DIST general-k is
  (leading hypothesis) `exp-chain(lnΓ_int(n+1) − lnΓ_int(k+1) −
  lnΓ_int(n−k+1) + k·lnp + (n−k)·lnq)` — the implied-argument decode of a
  BINOM pmf row reads a THREE-LGAMMA linear combination to ~0.02
  ULP-of-argument. Same integers recur across rows ⇒ overdetermined
  systems solve for per-integer internal-lgamma values bit-for-bit.
  Banked: b29 corpora + `lane2_binom_implied*.py` (the decode machinery).
  Every simpler lnC realization is REFUTED at the exact-bit level
  (see the lane-2 note section) — the ±2-ULP(arg) bell with uniform
  fractional part is the wall's own fingerprint.

## Wall 6/7/8 — POISSON k≥1, distribution pow, BETA.DIST probes

- **2026-07-18 (lane 1): wall 7 (distribution pow staging) is CLOSED** —
  `excel_pow_chain` landed, b27D 113/113, WEIBULL/EXPON signed off at
  99.983%/100.000% held-out. The POWER wrapper owns the 0.5→sqrt shortcut;
  the CRT pow underneath is the pure chain (story-grade: the shortcut is
  Excel's, not the C runtime's).
- ~~For wall 6 (POISSON k≥1 product staging): predicted x87-DR~~ —
  **superseded by lane 2 (2026-07-18)**: POISSON pmf is TWO routes (k=1 =
  extended-composed direct product, exact at large λ; k≥2 = Loader
  saddle-point dpois, bit-exact at λ ≳ 14; small-λ staging + branch
  structure open). The old "direct product proven / 21% unexplained"
  verdict was a route-blind-window artifact — withdrawn. See the lane-2
  note section for the full refutation ledger.
- BINOM cdf(0) ≡ pmf(0) bit-identical 1000/1000 (b24BT) — k=0 shares the
  pmf fast path, no bratio at k=0.
- Loader's dbinom x==0 branch is `(p < 0.1) ? -bd0(n,nq) - np : n·log(q)` —
  **SETTLED (b29b): Excel DOES flip below p=0.1** (bd0-form 383/400) — the
  Loader-control-flow smoking gun. 16 neither-rows = bd0-series/compose
  sub-staging, part of the bounded general-k enumeration.
- **2026-07-18 (lane 3): wall 8 first half CLOSED** — Excel has no
  integer-shape BETA.DIST special path (b30); A/B bounds staging broadly
  confirmed. Both OxFunc-side integer fast paths (gamma cdf, beta cdf)
  REMOVED from production.
- **GAMMA.DIST pdf MEASURED (b31, 4,750 rows banked) — new named wall:
  the closed-form-pdf extended-composition body class.** Triage REFUTED at
  the exact-bit level: production log-composed (16.1%), direct separate-pows
  (18%), ratio forms (22%), and R's dgamma-via-dpois structure (20% — NOT
  R's dgamma, unlike POISSON which IS Loader at k≥2). The sharpest read:
  a=1 (pdf = e^{−x/β}/β) fits the **reciprocal-based EXPON-style staging**
  (λ=1/β then λ·exp(−λx)) at 42.3% with a TIGHT ±1–2 residual — the same
  signature as POISSON k=1's extended-composed product (C4 class, ~70%).
  Hypothesis: POISSON small-λ, POISSON k=1, GAMMA.DIST pdf (and predictably
  CHISQ.DIST/BETA.DIST pdfs) share ONE legacy x87 body class whose
  extended-vs-spilled composition pattern is the single remaining unknown —
  crack it once, land it four times. Instruments ready: x87_serve
  mulex/mulee/pmfk ops + the b24/b31 banked corpora. Fractional-a b31F rows
  (1,000) additionally read the internal lgamma through stirlerr's
  non-integer branch if the dgamma road ever reopens.

- **2026-09-12 (local 12h last-bit, live Excel 16.0 build 20326/CV2 Value2):**
  - ERF/ERFC complement law on a fresh 2049-row signed grid: for `x>0`,
    `x<0.5` ⇒ `ERFC=1-ERF` (256/256 and 1031/1031 dense); `x>=0.5` ⇒
    `ERF=1-ERFC` (769/769). ERF is odd 100%. `ERFC(-x)=2-ERFC(x)` is exact
    1024/1024. Worksheet `EXP(-z*z)` matches identified `excel_exp` 1065/1065.
    Landing the wrapper against the current inexact bodies *regresses*
    (ERFC wrap 1264/2049 vs production 1320/2049; ERF `1-erfc` 1361 vs 1499).
    Do not land complement until the primary body is exact.
  - Firehorse Lentz `lentz/as714/n24 /mask=0400000` tail **1324**/bar 1283.
    Mid still `nswc_derfc0` 2389. Constraint, not identity. Pins inexact.
  - PRICE: Excel PRICE is 1 ULP above a worksheet `POWER` reconstruction on
    all 29 replica misses (private kernel, not worksheet POWER+SUM).
    Kahan/Neumaier/pairwise/Horner/geom all worse than the 571/600 native
    loop. `coup*(a/e)` is 571/600 vs production `(coup*a)/e` 564/600 on that
    corpus but is a corpus trade, not a universal graph.
  - Small-z ERF: 1800 NSWC/fdlibm store graphs, best 410/1031 (fdlibm x87
    continuous), max 3 ULP. Not an identity. libm::erf 405/1033.
  - GAMMALN Stirling `x>=8`: worksheet LN + x87 DR q/final-add is 1709/1711
    (two known 1-ULP rows). Landed as in-progress kernel; G3-02 remains open.
  - GAMMA positive integers: reverse native product matches live Excel
    `n=1..=88` (build 20326). Forward product breaks at 26. Reverse first
    miss at 89. Landed `1..=88` only; `n>=89` and non-integers remain open.
    `GAMMA != EXP(published GAMMALN)` on high-band integers (e.g. 8, 10).
    Half-integers `0.5..=15.5` match `(2n-1)!!/2^n * GAMMA(0.5)` seed
    `0x3ffc5bf891b4ef6b`. First miss 16.5. Worksheet `GAMMA` reflection
    `Γ(x)Γ(1-x)` vs `PI()/SIN(PI()*x)` is not bit-exact (typically 1–2 ULP).
  - GAMMALN B1 `[0.7,1.5)` live 512-row grid build 20326: production 124/512
    max 1182 (near-zero bit-distance at the Γ=1 zero). Still an op-graph wall.
  - PMT `answers-pmt-em.json`: production 10801/13752; `|tau|<1` 9649/12402.
    Invert-the-published-PMT implied `em` vs `excel_expm1_internal` is only
    7721/12402 — combine rounding pollutes the implied helper. Not a decode.
  - GAMMALN B2 `[1.5,4)` live 256-row build 20326: production 95/256 max 51.
    Composed `x<0.7`: 208/256 max 2. Worksheet LN instead of CRT log is only
    +1 exact (209/256); not landed. NEGBINOM.DIST(f,s,p,FALSE) vs
    `BINOM.DIST(f,f+s-1,1-p,FALSE)*p` is 3/10 — not an identity.
  - GAMMA half-integers: closed form through 15.5; live recurrence
    `GAMMA(x)==(x-1)*GAMMA(x-1)` is exact for `16.5..=19.5` (4/4) and
    first misses at 20.5 (1 ULP). Landed `16.5..=19.5` only.
  - GAMMA integers `89..=170`: vs reverse `FACT(n-1)` 4/82 (n=117,120,122,124),
    max 8 ULP, mean 4.6; vs worksheet `EXP(GAMMALN(n))` 0/82 max 979 ULP.
    Native product variants: best `blk4_rev` 15/82; x87 block-4 PC64
    store-between 16/82 max 27 ULP. Not an identity.
  - GAMMA tiny-x: `GAMMA(x)==1/x` on admitted `0 < x <= 1e-16` (decade grid
    plus 27-point neighborhood). Positive subnormals `#NUM!`. First miss
    `2e-16` (1 ULP). Landed that slice only.
  - HYPGEOM.DIST PMF is not worksheet COMBIN. Microsoft example
    `HYPGEOM.DIST(1,5,4,10,FALSE)=0x3fce79e79e79e79b` vs COMBIN `(C*C)/C` and
    `C*(C/C)` both `0x3fce79e79e79e79e` (3 ULP). Modest 20-row live grid
    0/20 vs both associations. Private kernel. (An earlier 9/9 was invalid:
    PowerShell `$n`/`$N` alias destroyed the population argument.)
  - MULTINOMIAL(a,b) is not COMBIN(a+b,a) (0/19, typically 1–many ULP).
  - POISSON k>=2 sqrt/div restage on b24 (k=1,2,3): production
    `exp/sqrt(2πx)` 2377/7998; x87_div / excel_sqrt / split-sqrt all 2377/7998
    (no gain); recip forms 1819/7998 worse. k=1 log-composed 1087/3999 still
    leads `λ*e^{-λ}` 1027. Sqrt staging remains a wall.
  - PRICE replica 29-miss accumulator race: worksheet-term native/Kahan/
    Neumaier/pairwise/reverse all 0/29 vs Excel. `nextup(sum+red-accr)` is
    only 16/29. Confirms private coupon-sum kernel, not a +1 ULP publication
    bump of the worksheet POWER reconstruction.
  - GAMMA peel-down `GAMMA(x)==GAMMA(x+1)/x` on a clean 128-row mixed grid
    is 93/128 max 17 ULP (typical miss 1 ULP). Not an identity; do not land
    a general peel.
  - PPMT+IPMT vs PMT on 15 live rows is 9/15 max 1 ULP. Not an identity.
  - GAMMA quarter-integers: recurrence from `GAMMA(0.25)` / `GAMMA(0.75)`
    is exact for `n=0..=5` (12/12 live). First miss 6.25/6.75. Landed that
    slice. Third-integer recurrence `n+1/3` was 7/21 max 8 ULP — not landed.
  - GAMMA odd eighths: `n+1/8` and `n+3/8` exact n=0..=3; `n+5/8` n=0..=2;
    `n+7/8` seed only. Landed those ranges.
  - GAMMA sixths: `n+1/6` recurrence 2/7 with n=1 already 1 ULP; `n+5/6`
    n=1 already 1 ULP (then scattered exacts). Not a contiguous seed
    family. Not landed.
  - GAMMA negative halves: `GAMMA(-0.5)` is 1 ULP from `-2*GAMMA(0.5)`.
    Peel `GAMMA(-1.5)=GAMMA(-0.5)/(-1.5)` is exact; `-2.5` already misses.
    Landed `-0.5` and `-1.5` only.
  - HYPGEOM.DIST PMF on a 20-row live modest grid: production choose_direct
    1/20 max 16 ULP; COMBIN `(C*C)/C` and `C*(C/C)` native/x87 0/20 max 14.
    Private kernel, close to COMBIN but not the worksheet graph.
  - CUMIPMT vs worksheet SUM of IPMT over the range is 2/8 max 6 ULP on a
    live 8-row grid (build 20326). Not an identity.
  - CUMPRINC vs worksheet SUM of PPMT is 3/8 max 3 ULP. Not an identity.
  - GAMMALN(n) vs LN(FACT(n-1)) for n=2..40 is 21/39 max 2 ULP. Not an
    identity; integer GAMMALN is the piecewise kernel, not LN of FACT.
  - GAMMA(n) vs EXP(LN(FACT(n-1))) for n=89..120 is 0/32 max 245 ULP,
    worse than reverse FACT (mean ~4.6 ULP). n>=89 is a product-rounding
    wall, not an exp/ln composition.
  - PDURATION is split worksheet LN `(LN(fv)-LN(pv))/LN(1+rate)` 80/80, not
    fused `LN(fv/pv)/LN(1+rate)` (20/80). Landed.
  - POISSON k=1 `excel_exp(-λ + excel_ln(λ))` is 1088/3999 vs native-ln
    1087/3999 (+1 exact). Not landed.
  - GEOMEAN vs EXP(AVERAGE(LN)) is 2/3 (third row 3 ULP). vs POWER 1/3.
    Not an identity.
  - GAMMA odd sixteenths in (0,1): live-pinned seeds; `GAMMA(1/16)` is 1 ULP
    from the generic path. Landed seeds only; recurrence not claimed.
  - F.DIST CDF vs worksheet BETA.DIST(d1*x/(d1*x+d2), d1/2, d2/2, TRUE) is
    2/3 with a 1 ULP miss. Argument construction rounding; not an identity.
  - T.DIST.2T vs F.DIST.RT(t^2,1,df) is 2/3 (one 2 ULP miss). Not an identity.
  - CONFIDENCE.T vs T.INV(1-α/2,n-1)*σ/√n associations: best `t*(σ/√n)` is
    3/6. Private kernel.
  - PMT(fv=0,type=0) vs worksheet `-pv*rate/(1-POWER(1+rate,-nper))` is 0/4
    max 4 ULP. Private kernel, not worksheet POWER annuity.
  - NPER(RATE(nper,pmt,pv), pmt, pv) is hundreds of ULP from nper (536 and
    156 on two live rows). RATE does not invert the published NPER graph.
  - NPV(IRR(cf), cf[1:])+cf0 is exact 0 on 2/5 live streams; the other three
    leave tiny nonzero residuals. IRR does not invert worksheet NPV.
  - F.INV vs worksheet `(d2/d1)*BETA.INV(p,d1/2,d2/2)/(1-BETA.INV)` is
    27/105 max 6317 ULP on a 15×7 live grid (build 20326). Nearby
    associations 25–29/105. Not an identity. FINV=F.INV.RT is 105/105
    (legacy alias). F.INV.RT vs F.INV(1-p) is 79/105 max 16 ULP.
  - T.INV.2T vs SQRT(F.INV.RT(p,1,df)) is 55/144. vs
    SQRT(df*(1/BETA.INV(p,df/2,0.5)-1)) is 135/135 for integer df>=2
    (worksheet BETA.INV) but production BETA.INV last-bit still blocks
    landing that composition (first miss T.INV.2T(0.02,2) 2 ULP).
  - T.INV.2T(p,1)=1/TAN(PI()*p/2) 9/9. T.INV(p,1)=T.INV.2T(2*(1-p),1).
    Landed the Cauchy df=1 slice.
  - T.INV.2T(p,2) closed forms best `SQRT(2*(1-p)*(1-p)/(p*(2-p)))` 6/9
    max 2 ULP. BETA.INV(p,1,0.5) vs `1-(1-p)^2` 3/9. Not identities.
  - GAMMA fifths recurrence n=1 already 1 ULP (2/11, 4/11, 6/11, 5/11).
    Landed (0,1) seeds only. Odd tenths in (0,1) also seed-only
    (`GAMMA(1/10)` 3 ULP from generic). Sevenths and 1/12,5/12,7/12,11/12
    likewise seed-only (`GAMMA(1/7)` 2 ULP from generic). Thirds and
    remaining ninths seed-only (`GAMMA(1/3)` 6 ULP from generic). Selected
    x in (-1,0) with exact worksheet peel are seed-only; IEEE
    GAMMA(2/3)/(-1/3) is 1 ULP from GAMMA(-1/3). GAMMALN=LN(GAMMA) exact
    at 1/5, 1/3, 1/7 (4/14 of a seed grid including 1/2); other seeds
    1–13 ULP.
  - ERF=ERF.PRECISE and ERFC=ERFC.PRECISE 16/16 on a signed z-grid
    (build 20326). ERFC=1-ERF 6/16 (only small |z|).
  - BETA.INV(p,1,b) vs 1-POWER(1-p,1/b) 23/42 max 96 ULP. Not an
    integer-shape inverse fast path.
  - LOGNORM.INV(p,m,s)=EXP(NORMSINV(p)*s+m) 27/27 and
    EXP(m+s*NORMSINV) 27/27; LOGINV alias 7/7. Production
    excel_exp(m+s*inv) is 1 ULP off the 0.1/0/1 pin (NORMSINV
    residual). Not landed.
  - NORMSINV=NORM.S.INV=NORM.INV(p,0,1) 9/9. Oddness
    NORMSINV(1-p)=-NORMSINV(p) 8/9 (p=0.05 is 5 ULP). T.INV(p,1e8)
    is not NORMSINV (1/9).
  - GAMMA.INV(p,1,scale) vs -scale*LN(1-p) 5/7 max 5 ULP. Exponential
    inverse is not the published GAMMA.INV a=1 graph.
  - GAMMA(n) vs (n-1)*GAMMA(n-1) for n=88..110 is 4/23 (scattered
    exacts at 91,92,94,95). Not a peel extension of the n=1..88 reverse
    product. FACT(n-1) 1/23.
  - PMT small-tau live 20326 grid (rate 1e-4..0.05, nper 12/24/60,
    pv=-1000, type=0): production is 1 ULP off the first pin
    PMT(1e-4,12,-1000). |tau|<1 helper remains a wall.
  - BETA.INV(p,a,1) vs POWER(p,1/a) 19/28 max 6 ULP. Not an identity.
  - GAMMALN B1 band production vs live 20326 capture 124/512 max 1182
    ULP. B1 coefficient wall unchanged.
  - GAMMA.DIST(x,1,1,TRUE) vs 1-EXP(-x) 5/6 (x=0.1 is 4 ULP). Not an
    identity.
  - ERF.PRECISE small-z live 20326 capture: production/libm 405/1033
    max 3 ULP. ERFC production 746/1033 max 3. NSWC native 55/1033.
    F-body still a constraint, not an identity.
  - TANH=SINH/COSH 8/8. EXP form 5/8. libm tanh 1 ULP off TANH(0.5).
    Landed the worksheet ratio.
  - SECH=1/COSH 5/5 and CSCH=1/SINH 5/5 (production already that
    graph; pinned). COTH vs COSH/SINH 5/9 max 1 ULP; COTH=1/TANH
    28/28 including COTH(800)=1. Landed 1/TANH.
  - ACOT vs PI()/2-ATAN 7/10 max 13 ULP (x=2 is 1 ULP). ACOT=ATAN2(x,1)
    28/28 including subnormal x and 1e300. Landed C atan2(1,x).
  - NORMSDIST(-1) live 20326 is 1 ULP from production (catalog G3-07
    leftover ERFC body). Aliases NORM.S.DIST/NORM.DIST(*,0,1,TRUE) 6/6.
  - BINOM.DIST(n,n,p,FALSE) vs POWER(p,n) 3/9 (only p=0.5). Not an
    identity.
  - ACOS vs PI()-ASIN is the wrong complement (0/9). ACOS=PI()/2-ASIN
    34/34 including the 0.75 ATAN2 miss. ATAN2 forms 11/14 max 1 ULP.
    libm acos is 1 ULP off ACOS(0.5). Landed PI()/2-ASIN.
  - T.DIST(x,1,FALSE)=1/(PI()*(1+x*x)) 20/20. Split 1/PI()/(1+x*x)
    12/20; 1/(PI()+PI()*x*x) 18/20. T.DIST CDF Cauchy 0.5+ATAN/PI
    6/9 max 4 ULP. T.DIST df=2 closed forms not identities.
  - CHISQ.DIST.RT(x,4) vs EXP(-x/2)*(1+x/2) 7/9 max 1 ULP. df=6
    Poisson polynomial 7/9. Not identities.
  - BETA.DIST(x,1,2,TRUE) vs 1-(1-x)^2 15/18 max 8 ULP on a wider
    grid (first miss x=0.01). BETA.DIST(x,2,1) vs x^2 12/18.
    BETA.DIST(x,1,1) vs x 14/18. Not integer-shape fast paths.
  - ATAN2 Range.Value2 inject flushes subnormals, 1e-308, and
    double.Epsilon to +0 before the formula runs. Apparent ATAN2
    DAZ evidence on those rows is an injection artifact. Overflow
    #NUM! at ATAN2(1e-200,1e109) still holds on normals.
  - F.DIST.RT(x,2,d2) vs POWER(d2/(d2+2x),d2/2) 3/9 max 2 ULP.
  - CONFIDENCE.NORM vs NORMSINV(1-α/2)*σ/SQRT(n) 3/6 max 1 ULP.
    CONFIDENCE alias 6/6.
  - BINOM.DIST(0,n,p,FALSE) vs POWER(1-p,n) 1/9 max 5 ULP.
  - T.DIST.RT(x,1) vs 0.5-ATAN(x)/PI() 4/9. vs ACOT/PI() 5/9.
  - POISSON PMF recurrence P(k-1)*λ/k 9/20 max 3 ULP. k=1
    EXP(LN(λ)-λ) 7/10. FACT/POWER forms 8/20.
  - TAN vs SIN/COS 3/10 max 1 ULP. COT=1/TAN 10/10 (production
    already x87 recip of TAN; pinned).
  - BINOM vs COMBIN*POWER*POWER 1/8 max 9 ULP.
  - T.DIST.2T vs 2*T.DIST.RT 15/15 across df=1..60. Production
    already uses that association; leftover is the RT/bratio
    body (T.DIST.2T(1,1) production 9 ULP from Excel).
  - T.DIST.RT(x,1)=T.DIST(-x,1,TRUE) 8/8. CDF complement
    1-T.DIST is 2/8. CHISQ.DIST.RT vs 1-CHISQ.DIST df=1 2/8.
  - LOG10 vs LOG(x,10) 3/7. vs LN/LN(10) 3/7.
  - RRI vs POWER(fv/pv,1/nper)-1 5/6 max 4 ULP.
  - WEIBULL.DIST(x,1,b) vs EXPON.DIST(x,1/b) CDF 6/7 PDF 6/7.
  - PERMUT vs FACT(n)/FACT(n-k) 6/8 max 1 ULP on a FACT-rounding
    grid (known non-identity; production is the x87 product).
  - GAMMA.DIST integer pdf vs EXP*POWER/FACT 0/6. CDF vs
    1-POISSON.DIST(a-1,x,TRUE) 4/6.
  - ERF.PRECISE(z)=GAMMA.DIST(z*z,0.5,1,TRUE) 7/7 and
    ERFC.PRECISE(z)=CHISQ.DIST.RT(2*z*z,1) 7/7. Circular with
    the identified a=0.5/df=1 ERF/ERFC dispatch; not a new body.
  - NORM.DIST vs NORMSDIST((x-m)/s) 9/9 (production already
    that compose; leftover NORMSDIST(-1) is the ERFC body).
  - GAMMA(n+0.5) stepwise recurrence first miss 20.5 (1 ULP).
    Product-first (0.5*...* (n-0.5))*GAMMA(0.5) is 172/172 through
    171.5 including 20.5; GAMMA(172.5)=#NUM!. Landed.
  - NEGBINOM PMF vs COMBIN*POWER 1/8; vs BINOM*p 2/8.
  - SEC=1/COS 8/8 and CSC=1/SIN 8/8 (production already those
    graphs).
  - GAMMA(n+1/4) product-first contiguous through 9.25 (n=0..=9);
    first miss 10.25. Landed. GAMMA(n+3/4) product-first misses
    2.75; keep recurrence n=0..=5.
  - GAMMA odd eighths product-first: n+1/8, n+3/8, n+5/8 through
    n=9; n+7/8 misses 1.875. Landed the three extending families.
  - GAMMA odd sixteenths product-first from (0,1) seeds: 1/16 n<=9,
    5/16 n<=4, 9/16 n<=10, 13/16 n<=5. Other four miss at n=1.
  - GAMMA product-first from remaining (0,1) seeds: 1/12 and 5/12
    n<=1, 7/12 n<=3, 1/7 n<=2, 3/10 n<=1. 11/12 and other tenths/
    sevenths miss at n=1.
  - GAMMA 1/13 product-first n<=2; 1/5 n<=1. 1/11, 1/17, 1/9 miss n=1.
  - GAMMA elevenths product-first: 2/11,3/11,6/11 n<=1; 4/11 n<=2;
    7/11,9/11,10/11 n<=3. 1/11,5/11,8/11 miss n=1.
  - GAMMA thirteenths product-first: 2/13 n<=3, 3/13 n<=2, 4/13 n<=1,
    6/13 n<=3, 7/13 n<=4, 9/13 n<=4, 11/13 n<=1. 5/13,8/13,10/13,12/13
    miss n=1.
  - GAMMA seventeenths product-first: 3/17,4/17,5/17,16/17 n<=1;
    7/17..=12/17 and 15/17 n<=3. 1/17,2/17,6/17,13/17,14/17 miss n=1.
  - GAMMA ninths product-first: 5/9 n<=3, 7/9 n<=1. 1/9,2/9,4/9,8/9
    miss n=1.
  - GAMMA 1/3 and 2/3 product-first miss n=1. 2/5,3/5,4/5 miss n=1.
  - PMT vs POWER annuity 0/6 max thousands of ULP on small-tau;
    vs EXP/LN 0/6. |tau|<1 helper still a wall.
  - COSH=(EXP+EXP(-))/2 40/40 spilled and fused; libm 1 ULP off at
    0.001, 0.01, 10. Landed. SECH follows 1/COSH.
  - SINH worksheet EXP-pair 27/40. Internal Kahan expm1 pair
    (expm1(x)-expm1(-x))/2 is 37/37 including those misses. Landed.
    CSCH follows 1/SINH.
  - TANH vs SINH/COSH 35/40 on the wider COSH grid (misses 0.001,
    0.01, 0.4 and sign mirrors). Earlier 8/8 pin set still holds;
    not a universal last-bit identity.
  - TAN vs SIN/COS 9/17 max 1 ULP (wider grid). Not an identity.
  - IPMT(per=1,type=0) vs worksheet -(pv*rate) 7/10 (the 7 are the
    type=0 per=1 rows). PMT=IPMT+PPMT 10/10. IEEE and x87
    -(pv*r) match Excel IPMT 4/7; 0.01*1000 stays 1 ULP
    (Excel 0xc023ffffffffffff vs IEEE -10). First-period multiply
    is not a full landing.
  - T.DIST(x,1,TRUE) vs 0.5+ATAN(x)/PI(): a COM ulp helper that
    cast int64 bit patterns to double collapsed 1-ULP misses to 0
    (false 13/13). IEEE/x87 reconstructions of spilled libm atan
    are 8/13 vs live bits (x=-1 is 1 ULP). Not landed.
  - GAMMA(0.5)=SQRT(PI()) and GAMMALN(0.5)=LN(SQRT(PI()))=0.5*LN(PI())
    in Excel. IEEE sqrt(pi) is 1 ULP below the published GAMMA(0.5)
    seed; keep the seed.
  - ERF.PRECISE tiny: 2x/SQRT(PI) 1/12; Taylor3 3/12;
    2*NORMSDIST(x*SQRT(2))-1 9/12 (misses z<=1e-4, leftover
    NORMSDIST/ERFC body). 1-ERFC 9/12.
  - T.DIST(x,2,FALSE)=POWER(2+x*x,-1.5) 15/15; excel_pow_chain
    15/15. Landed.
  - F.DIST.RT(x,2,d2) vs POWER(d2/(d2+2x),d2/2): dedicated
    Value2 capture at (0.5,2,2) is 1 ULP (RT 0x3fe5555555555556,
    POWER/2/3 0x3fe5555555555555). excel_pow_chain 14/15 on a
    15-row subset. Not an identity.
  - CHISQ.DIST.RT df=4 vs EXP(-x/2)*(1+x/2): spilled excel_exp
    5/7. Not landed. The earlier 7/7 Excel score used the broken
    ulp helper.
  - T.DIST df=3 PDF closed forms scored 15/15 only under the
    broken ulp helper; rust reconstructions 0-5/15. Not landed.
  - BINOM k=0 vs POWER(1-p,n) and POISSON k=1 vs lambda*EXP(-lambda)
    scored 12/12 only under the broken ulp helper. Honest uint64
    distance: BINOM k=0 POWER 3/12 (only p=0.5); POISSON k=1
    lambda*EXP 1/12; EXP(LN-lambda) 4/12. Not landed.
  - TANH vs SINH/COSH honest 8/11 (misses 0.001, 0.01, 0.4 by 1 ULP).
    Cubic only |x|<=1e-4. EXP form 3/11.
  - CHISQ.DIST.RT df=4 vs EXP(-x/2)*(1+x/2) honest 7/9 (x=0.1 and
    x=2 are 1 ULP). df=6 Poisson poly 7/9.
  - GAMMA.DIST(x,1,1,TRUE)=EXPON.DIST(x,1,TRUE) 12/12 (already
    production). PDF vs EXP 5/12; CDF vs 1-EXP 9/12.
  - LOGNORM.DIST CDF vs NORMSDIST((LN-m)/s) 8/8 honest (already
    production compose). PDF vs NORM.S.DIST/(x*s) 2/8.
  - NEGBINOM vs BINOM(k,k+s-1,1-p)*p 4/8. vs COMBIN*POWER*POWER 1/8.
  - T.DIST df=4 PDF POWER closed forms 0-3/15. Not identities.
  - F.DIST.RT d1=2 vs POWER(d2/(d2+2x),d2/2) honest 6/9 (1-2 ULP
    misses including (0.5,2)). Not an identity.
  - BINOM k=1 vs n*p*POWER(1-p,n-1) honest 3/10; vs EXP/LN 2/10.
  - F.DIST(x,2,2,FALSE) vs 1/(1+x)^2 honest 4/10. F.DIST.RT(x,2,2)
    vs 1/(1+x) 6/10. CHISQ df=4 x87_mul(exp,1+h) still 7/9.
  - CHISQ.DIST(x,2,FALSE) vs 0.5*EXP(-x/2) honest 6/10. CDF vs
    GAMMA.DIST(x,1,2,TRUE) 10/10 (already production). vs 1-EXP 7/10.
  - BETA.DIST(x,2,2,FALSE) vs 6x(1-x) honest 3/10. CDF vs x^2*(3-2x)
    6/10. Confirms no integer-shape beta fast path.
  - T.DIST(x,1,TRUE) honest: 0.5+ATAN/PI 8/13; (PI/2+ATAN)/PI 8/13;
    ACOT(-x)/PI 10/13. Not identities.
  - WEIBULL.DIST(x,1,b) vs EXPON.DIST(x,1/b) honest CDF 8/8 PDF 7/8
    (b=3 PDF is 1 ULP). Bodies already signed off; leftover last-bit
    on inexact 1/b PDF.
  - NORM.S.DIST pdf vs PHI 10/10 and vs EXP(-x^2/2)/SQRT(2PI) 10/10
    (PHI already signed off). NORMSDIST vs 0.5*(1+ERF.PRECISE(x/SQRT2))
    6/10 leftover ERFC body.
  - FISHERINV vs TANH honest 6/9. FISHER(TANH(y)) vs y 4/9. Not
    identities.
  - CHISQ.INV.RT(p,2) / CHIINV(p,2) vs worksheet -2*LN(p) honest 17/18
    (p=0.8 is 1 ULP) and dense 54/65 max 1 ULP (misses 0.65, 0.8, 0.85,
    0.92 and 0.8-neighborhood). Forward EXP(-x/2) recovers p only 14/18,
    so the inverse is not invert-EXP. Not landed. CHISQ.INV(p,2)=
    GAMMA.INV(p,1,2) 18/18 but neither is -2*LN(1-p) (11/18).
  - T.INV.2T(p,2) vs (1-p)*SQRT(2/(p*(2-p))) honest 7/18 max 18 ULP.
    T.INV(p,2) vs (2p-1)*SQRT(...) 3/18. T.DIST.2T vs 1-|x|/SQRT(2+x^2)
    2/11. Not identities.
  - F.INV(p,2,2) vs p/(1-p) 9/18; F.INV.RT vs (1-p)/p 8/18. FINV =
    F.INV.RT 18/18. F.INV(p,2,4) vs 2*(1/SQRT(1-p)-1) 2/18.
  - GAMMALN(x+1) vs GAMMALN(x)+LN(x) 0/10 max 27 ULP on landed seeds.
  - FACT(n)=GAMMA(n+1) honest 14/14 on n in 1..87 (already-production
    reverse product; GAMMA integers stop at 88).
  - POISSON k=1 vs EXP(LN(lam)-lam) honest 7/11 max 3 ULP; vs lam*EXP
    4/11. k=2 closed forms 4-5/11. Not identities.
  - ERF.PRECISE+ERFC.PRECISE vs 1 honest 8/10 max 1 ULP. ERF vs 1-ERFC
    6/10. ERFC vs 1-ERF 5/10 max 15830 (cancellation). Not identities.
  - BINOM.DIST CDF vs BETA.DIST(1-p,n-k,k+1) 7/10 max 3 ULP. vs
    1-BETA.DIST(p,k+1,n-k) 7/10. Not identities.
  - BETA.INV(p,1,1) vs p 12/17 max 2 ULP. (p,1,2) vs 1-SQRT(1-p) 6/17.
    (p,2,1) vs SQRT(p) 9/17. (p,5,1) vs POWER(p,1/5) 14/17 max 1 ULP.
    GAMMA.INV(p,1,1) vs -LN(1-p) 11/17. Not identities.
  - CHISQ.DIST(x,k,FALSE)=GAMMA.DIST(x,k/2,2,FALSE) for df=2,4,6 (10/10).
    df=2 x>0 also 13/13. 0.5*RT / 0.5*EXP 8/12 max 1 ULP. EXPON.DIST(x,0.5)
    10/14. Production libm CHISQ PDF is 5–8 ULP vs Excel; production
    GAMMA.DIST PDF is 4–7 ULP. Excel identity is real; neither production
    kernel is the Excel last-bit graph.
  - T.DIST df=2 CDF vs 0.5+0.5x/SQRT 3/12 max 40 ULP. (SQRT+x)/(2*SQRT)
    4/12. Not identities. GAMMA.DIST a=2 PDF vs x*EXP(-x) 6/12.
  - NEGBINOM k=1 vs s*POWER(p,s)*(1-p) 4/10 max 4 ULP. vs
    NEGBINOM(0)*s*(1-p) 3/10. vs BINOM(s,s+1,p) 0/10. Not identities.
  - FACTDOUBLE(2n)=POWER(2,n)*FACT(n) 11/11 (already-production even
    double-factorial). FACTDOUBLE(2n-1) vs GAMMA(n+0.5)*2^n/SQRT(PI)
    1/11 max 2 ULP.
  - MULTINOMIAL(a,b) vs COMBIN(a+b,a) 1/10 max 22 ULP. vs FACT ratio
    0/10. Excel MULTINOMIAL sits 1–21 ULP below COMBIN. Not identities.
  - IMARGUMENT vs ATAN2(re,im) 10/10 (already-production atan2).
    IMABS vs SQRT(re^2+im^2) 9/10 max 1 ULP. IMEXP vs EXP*COS/SIN
    IMREAL 1/10 max 22 ULP, IMAGINARY 2/10 max 12 ULP. Not the
    worksheet elementary graph.
  - CUMIPMT vs sum of IPMT over the range honest 1/3 (15 and 7 ULP
    misses). CUMPRINC vs sum of PPMT 1/3 max 1 ULP. Not identities.
  - BETA.DIST PDF a=1 b=2 vs 2*(1-x) 6/9 max 1 ULP. a=2 b=1 vs 2x 7/9.
    a=1 b=3 vs 3*(1-x)^2 3/9. CDF a=1 b=2 vs 1-(1-x)^2 8/9. Confirms
    no integer-shape beta closed form.
  - T.DIST df=3 PDF worksheet POWER closed forms honest 1–4/20
    (best POWER(-2)*2/(PI*SQRT3) 4/20). df=4 (3/8)*POWER 4/20.
    Not identities.
  - F.DIST.RT(x,2,d2) vs EXP((d2/2)*LN(d2/(d2+2x))) honest 56/81;
    POWER 36/81; 1/POWER 28/81. CDF 1-POWER 49/81. PDF POWER 18/81.
    Not identities.
  - GAMMALN=LN(GAMMA) at product-first n>=1 points of landed (0,1)
    seeds: 13/72, and those 13 are already in GAMMALN_LN_GAMMA_X.
    No new LN(GAMMA) exacts in that sweep.
  - 32nd first peels 1/32,3/32,15/32,17/32,31/32 are worksheet-exact
    into (-1,0); skipped as a new unseeded family (same rule as
    sixths/14ths/19ths). 1/6-2 is worksheet-exact but 1/6-1 misses
    1 ULP; sixths stay unseeded.
  - T.DIST df=3 excel_pow_chain closed forms 2–7/20 vs live bits
    (best 2/(PI*SQRT3)/POWER 7/20). Not an identity.
  - CHISQ.DIST(x,2,FALSE)=GAMMA.DIST(x,1,2,FALSE) 9/9. vs
    EXPON.DIST(x,0.5,FALSE) 7/10. vs 0.5*excel_exp(-x/2) 6/10
    including x87_mul associations. GAMMA.DIST a=1 PDF vs
    EXPON(x/b,1)/b 33/63. Excel identity is real; production PDF
    leftover remains.
  - F.DIST.RT d1=2 excel_pow_chain and excel_exp*log 11/16 vs live
    bits; split POWER 3/16. Not identities.
  - CHISQ.DIST(x,1,FALSE)=GAMMA.DIST(x,0.5,2,FALSE) 10/10. Closed
    forms EXP/SQRT(2xPI) 2/10, 1/SQRT*EXP 4/10, PHI(SQRT)/SQRT 2/10.
    3/5 peels stop after -8 ( -9 miss 1 ULP). 1/16 peels stop after
    -6 ( -7 miss 1 ULP).
  - CHISQ PDF df=1 excel_exp/sqrt associations 2–3/10 vs live bits.
    IMLOG10 vs IMLN/LN(10) 2/10 re and im; vs LOG10(IMABS) 2/10;
    IMLOG2 vs IMLN/LN(2) 2/10. Not worksheet-log identities.
  - T.DIST df=2 CDF vs 0.5+0.5x/SQRT(2+x*x) 8/16; vs
    (SQRT+x)/(2*SQRT) 9/16. RT 0.5-0.5|x|/SQRT 5/16. Not identities.
  - IMCOS re vs COS*COSH 0/10; IMSIN re vs SIN*COSH 1/10; IMCOSH re
    vs COS(y)*COSH(x) 0/10. Private complex kernels, not worksheet
    trig/hyperbolic products.
  - GAMMA.DIST(x,2,1,FALSE) vs x*excel_exp(-x) 4/10 including x87_mul.
  - BINOM.DIST.RANGE(n,p,0,k)=BINOM.DIST(k,n,p,TRUE) 48/48 and
    RANGE(n,p,k)=BINOM.DIST(k,n,p,FALSE) 48/48 live 20326. Production
    BINOM CDF is 1 ULP off Excel at (10,0.3,4), so RANGE cannot inherit
    the CDF graph until the BINOM body is exact.
  - PERMUT vs COMBIN*FACT 19/20 (n=20 k=5 is 1 ULP). vs FACT/FACT 20/20
    (already-known Excel identity; production is the x87 product).
    PERMUTATIONA vs n^k 20/20 (production already powi).
  - STDEV.S=SQRT(VAR.S) 5/5 and STDEV.P=SQRT(VAR.P) 5/5 (already the
    production compose). DEVSQ vs VAR.S*(n-1) 3/5.
  - BETA.DIST(x,0.5,0.5,TRUE) vs 2*ASIN(SQRT(x))/PI() 7/9. PDF vs
    1/(PI*SQRT(x(1-x))) 3/9. Not identities.
  - F.DIST(x,4,4,FALSE) vs 6x/(1+x)^4 3/8. CDF/RT 1/(1+x)^2 forms
    0/8 (wrong closed form). WEIBULL a=2 vs worksheet EXP/EXPM1 0/20
    (private body already identified as x87 pow/exp, not worksheet).
  - NEGBINOM.DIST(k,s,p,TRUE)=BETA.DIST(p,s,k+1,TRUE) 45/45 (already
    production regularized_beta). vs 1-BINOM 30/45.
  - ISPMT vs pv*rate*(per/nper-1) 4/6 max 1 ULP (production is that
    IEEE formula).
  - T.DIST df=5 PDF POWER closed forms 1/8. IMPOWER vs IMEXP(n*IMLN)
    0/6. GAMMA.DIST a=0.5 b=1 PDF vs EXP(-x)/SQRT(PI*x) 2/8.
    LOG(x,EXP(1))=LN(x) 8/8 (already production ln/ln(base)).
  - CHISQ.DIST.RT df=3 vs ERFC.PRECISE(SQRT(x/2))+SQRT(2x/PI)*EXP 4/7.
    PDF vs SQRT(x/(2PI))*EXP 2/7. F.DIST.RT(x,1,d2) vs T.DIST.2T(SQRT(x),d2)
    20/25. Zero-coupon PRICE vs red/POWER(1+yld/freq,freq*YEARFRAC) is
    exact on two 30/360 rows and far off on actual/actual — not a
    general PRICE graph.
  - BETA.INV(p,0.5,0.5) vs SIN(p*PI/2)^2 4/8; vs (1-COS(p*PI))/2 6/8.
  - SQRTPI(x)=SQRT(PI()*x) 8/8 (already production n*π then pow 0.5).
    Split SQRT(PI())*SQRT(x) 5/8.
  - GAMMA.DIST(x,3,1,FALSE) vs x*x*EXP(-x)/2 1/7. CDF Poisson-poly 1/7.
  - POISSON k=0 PMF=EXP(-lam)=CDF 9/9 (already production excel_exp).
    k=1 vs lam*EXP 3/9.
  - RATE(1,pmt,pv) vs -pmt/pv-1 2/6 (iterative even at nper=1).
  - Product-first nmax+1 for 1/7, 3/10, 7/11, 9/16, 1/16, 5/9, 7/12
    all miss 1–4 ULP. Contiguous nmax already tight; do not extend.
    7/13 was the exception (extended through n=6). IMSEC vs 1/IMCOS 0/5.
  - PMT type=1 vs type=0/(1+rate) 2/5 max 2 ULP. Not a last-bit identity.
  - Odd-eighth product-first n=10 misses 1–2 ULP; n=9 remains the
    contiguous nmax.
  - GAMMALN B1 two-step `GAMMALN(x)==GAMMALN(x+1)-LN(x)` 35/181
    (`[0.7,1)` 19/73; `(1,1.5)` 16/108). LN(GAMMA) 6/181. Not a
    B1 reduction.
  - NEGBINOM PMF vs BINOM identities: `BINOM(s,k+s-1,p)` 2/346;
    `BINOM(k,k+s-1,1-p)*p` 107/346 then 61/180; `BINOM*(1-p)` 9/180;
    COMBIN/POWER forms 37–39/180. k=1 vs `NB0*s*(1-p)` 19/72. Private
    PMF leftover.
  - BINOM k=0 vs worksheet POWER 14/72; vs EXP(n*LN(1-p)) 49/72.
    Rust excel_exp/pow_chain 132/210; production 146/210 (p<0.1 bd0
    17/30). Do not replace production k=0.
  - ERFC.PRECISE vs 1-ERF.PRECISE is exact on positive `(0, 0.5]`
    (1033/1033) and not on negatives (237/256 in `[-0.5,0)`). Positive
    slice landed; remaining ERFC is the ERF body plus mid/tail F-body.
  - Small-z ERF body: libm/fdlibm 405/1033; x87-continuous fdlibm
    411/1033; NSWC 55; nextafter+inf 463 (shifts the −1 ULP bin, not
    a graph). Rational LS fits worse. Body remains open.
  - PMT fv=0 type=0 live 330-row invert: production 156/330; `|tau|<1`
    93/264; implied em vs Kahan 63/264. Alternate Kahan orderings do
    not beat `(u-1)*t/ln u`. Combine still pollutes the helper.
  - POISSON k=1 live 56-row: production log-compose 38/56; `λ*e^{-λ}`
    29/56; excel_ln vs native ln tie. k=1 leftover is the exp chain.
  - BINOM k=0 live 210-row: production 146/210 beats pow_chain/EXP/LN
    132/210. Keep the p<0.1 bd0 branch.
  - BINOM CDF vs BETA.DIST(1-p,n-k,k+1) 199/240 (1 ULP misses).
    RANGE=CDF 246/246 already known. CDF is not published BETA.
  - NEGBINOM large-n (k+s-1>200) 0/48 vs production and vs excel_log
    / excel_exp / pow_chain composes. Private PMF.
  - GAMMA.DIST a=2 CDF vs 1-EXP(-x)*(1+x) 12/55; vs 1-POISSON(1,x)
    29/55. PDF vs x*EXP 22/55. Integer-a closed forms are not the
    graph.
  - T.DIST df=2 CDF closed form 0.5+x/(2*sqrt(2+x*x)) 46/75 rust
    (worksheet 32/53); production 39/75. Not an identity.
  - F(2,2) RT production already 32/32 on the live grid; 1/(1+x)
    25/32. CDF closed forms 21–24/32 vs production 29/32.
  - GAMMALN two open Stirling rows: q-chain associations 0–1/2;
    nextup of production is 2/2 but is not a graph (would regress
    the 1709 exact high-band rows).
  - BINOM k=n: worksheet POWER 12/35 mixed and 14/40 high-p, but
    `excel_pow_chain(p,n)` is 35/35 and 40/40 including q<0.1.
    Landed; k=0 bd0 branch unchanged (production 146/210 still
    beats pow_chain 132/210 on k=0).
  - CHIINV.RT df=2 vs -2*LN(p) 34/39 (1 ULP misses). Not a slice.
  - RATE(1,pmt,pv) vs -pmt/pv-1 21/24 live 20326 (production 2/24).
    Misses include pmt=-pv (Excel tiny vs closed 0) and two 1-ULP
    rows. type=1 vs -pmt/(pv+pmt)-1 0/24. Not a last-bit identity.
  - IRR of two cashflows vs fv/(-pv)-1 5/6 (1 ULP at 1200/-1000).
  - HYPGEOM modest 0/8 vs choose product (max 9 ULP); div-first
    choose 1/8. Private PMF.
  - T.DIST.2T==2*T.DIST.RT 20/20 (already production 2*0.5*bratio).
  - NEGBINOM modest C*pow_chain 8–12/48 vs production 11/48.
