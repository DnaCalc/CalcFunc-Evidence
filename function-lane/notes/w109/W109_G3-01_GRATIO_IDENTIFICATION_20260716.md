# W109 G3-01 — Distribution substrate identified as the DCDFLIB/NSWC GRATIO family (2026-07-16)

Status: **major identification, not yet bit-closed.** The incomplete-gamma side of the
G3-01 distribution substrate is the **TOMS 654 GRATIO branch structure (DiDonato &
Morris / A. H. Morris, NSWC), compiled in plain SSE2 double** — NOT an x87-extended
continued fraction as the 2026-07-14 sweep hypothesized. The remaining unknowns are
reduced to three named sub-identifications (Excel-internal erf/erfc, the internal
Γ/lgamma normalizer, Taylor-path micro-staging) plus the beta-side sibling (BRATIO,
TOMS 708, unprobed).

Work dir (gitignored, captures + harness): `smart-fuzzer/work/w109/G3-01-dist/`
Racer binary (tracked): `smart-fuzzer/tools/calc_graph_racer/src/bin/check_igamma.rs`
All live-Excel answers are also in the persistent OracleCache.

## The multi-view collapse (battery B1, 829 probes, build 20131)

- Legacy ≡ modern bit-for-bit everywhere probed: CHIDIST≡CHISQ.DIST.RT,
  FDIST≡F.DIST.RT, TDIST(·,·,1)≡T.DIST.RT, GAMMADIST≡GAMMA.DIST, BETADIST≡BETA.DIST.
- GAMMA.DIST beta-scaling is transparent for exact transforms (β=1 vs β=2 at doubled
  x agree 33/33) → one internal P(a, y), y = x/β double-divided first.
- CHIDIST is NOT RN53(1 − published P) (16 eq / 17 ne) → Q has its own publication.
- Deviation-from-correctly-rounded propagates IDENTICALLY through views → one kernel.

## Key evidence chain

1. **Excel ~67% CR-exact overall** with |δ| up to 47; δ magnitude scales like
   |a·ln x|·2⁻⁵³ → double-rounded exp-argument (battery-1/2 deviation map).
2. **Implied-argument decode** (`arg_fit.py`): at a=3 the argument error equals the
   exact rounding residue of `R53(R64(3·R53(ln x) − x))` on every row (double log,
   double argument); at a=2 it is ~2× the ln residue; **at a=1 the argument is clean
   of ANY double-rounding** — impossible for one code path…
3. **…because a==1 is a dispatch**: `a=1+2⁻²⁰` is NOT clean (battery-5), and the
   a=1 slice fits the exponential-CDF closed form (−expm1(−x) family): wrapper race
   179/205 vs 143/205 without. GAMMA.DIST(x,1,β) IS the exponential CDF.
4. **Faithful GRATIO transcription** (`cdflib_py.py`, from the scipy v0.14 cdflib
   Fortran) races at 416/692 overall, with the match rate concentrated exactly where
   GRATIO's branch map predicts (`gratio_detail.py`):
   - `closed-int` (integer a, a ≤ x < 31: finite exp(−x)·Σxᵏ/k!): **199/218 = 91%**
   - `asymp` (x ≥ 31): 4/6; `temme` (a ≥ 20, a=15 via the |a|≥15 gamma branch): 5/5
   - `taylor` (x ≤ max(a, ln10), the wk[20] backward-tail series): 48% with small
     per-a biases — normalizer + micro-staging residual
   - `closed-halfint` (erfc1-based) and `erf(a=1/2)` routes: fail ±1..±24 → Excel
     uses ITS OWN erf/erfc, not the NSWC rationals.
5. **Normalizer**: NSWC `gamma()` value error (~8e-15 rel at a=2.75) explains the
   constant +32..+42 offsets at fractional a; CR-Γ improves (a=1.25: 0→10/20) but is
   not exact either; a=4/6 (Γ exact) still miss → independent Taylor micro-staging
   residual. The internal Γ/lgamma is the same unknown as G3-02 — this lane now gives
   a per-a MEASUREMENT channel for it (each (a, many-x) slice over-determines the
   internal normalizer value).
6. **Excel's erf is near-CR** (ERF.PRECISE 158/176 CR-exact, ±1-2 tails): NSWC ruled
   out (113/176, regime flip at its 0.5 boundary), Cody SPECFUN CALERF ruled out
   (121/176 erf, 56/176 erfc, both exp models). 352 ladder points captured
   (`answers-erfp/erfcp.json`). Next candidates: fdlibm s_erf/s_erfc, Boost.
   ERF.PRECISE/ERFC.PRECISE/GAUSS (G4-04/G3-07) get closed by the same sub-lane.

## Corrections to prior claims

- The 2026-07-14 sweep verdict "x87 80-bit EXTENDED kernel; fix = x87-extended CF"
  is WRONG. The extended-precision convergence analysis only proved the CF converges;
  the kernel is plain double with the GRATIO branch structure. (The catastrophic
  6224-ULP CHIDIST row is OxFunc's plain-double NR complement, not an Excel-side
  extended CF — Excel's closed-int branch avoids the cancellation entirely.)
- "Distributions = one incomplete-γ CF kernel" under-described the structure: five
  branches (closed-int / closed-halfint / Taylor / CF / Temme) + the a==1 and a==0.5
  dispatches.

## erf sub-lane findings (2026-07-17 session)

**Wiring PROVEN by cross-view**: `GAMMA.DIST(k²/1024, ½, 1, TRUE) ≡ ERF.PRECISE(k/32)`
and `CHIDIST(k²/512, 1) ≡ ERFC.PRECISE(k/32)` — **160/160 AND 160/160 bit-exact**
(`answers-xv-gd/xv-chi.json`). The gratio a=0.5 dispatch calls exactly the published
ERF.PRECISE/ERFC.PRECISE routines; one identification closes all of them + CHIDIST
odd-df + half-integer paths.

**Architecture PINNED, tables custom.** Ruled out bit-exactly: NSWC (113/176 erf),
Cody SPECFUN CALERF (121/176), fdlibm s_erf (160/176 — closest but ±2), Boost
1.35–1.42 erf_imp<53> (155-157/176; tables identical across versions), and the local
Microsoft UCRT erf (146/176) — all with CR/fdlibm/x87 exp models. Established:
- **erfc computes exp(−RN53(z·z)) with an UNSPLIT argument** — proven by regression
  of the messy-grid (full-mantissa z) residual against the exactly-computable
  RN53(z·z) rounding error: slope +0.95, residual stdev 7.9e-16 → 2.0e-16 (±1 ULP
  floor). This kills all split-argument families (fdlibm/Cody) structurally.
  CAUTION (method): the original k/32 ladder had EXACT z² everywhere — dyadic-clean
  grids can make split-vs-unsplit invisible; always add a full-mantissa grid.
- **No tiny-z shortcut** (Boost's z<1e-10 form ruled out): tiny-z rows are consistently
  CR+1, and 12/15 give the SAME ratio double — the small branch's value at 0 is
  pinned exactly: **R(0⁺) = 0x3ff20dd750429b6e = CR(2/√π)+1 ULP**.
- **No Boost 5.8f erf→1 cutoff** (CR, not 1.0, just above 5.8f). erf = 1−erfc above
  the small branch (long CR-exact run for z ≥ 1.375 on the clean grid).
- **Small-branch/complement boundary at 0.5** (messy crossing scan consistent).
- The apparent erfc hard-zero in (26.543, 26.544] is NOT a Cody XBIG: the last
  finite witness sits in the smallest normal binade (0x001…) — it is the known
  Excel-wide **subnormal publication flush** (same as the PHI lane's pinned flush).
- Detrended erfc residual is a flat ±1-ULP evaluation floor across [0.5, 6] — a
  uniform-quality rational (or intervals of equal quality; no sharp boundary signal
  at Boost's 1.5/2.5/4.5 or fdlibm's 1.25/2.857).

Data: `answers-erfp/erfcp.json` (clean k/32 ladders), `answers-erfm/erfcm.json`
(full-mantissa), `answers-b7erf/b7erfc.json` (lineage fingerprints),
`answers-b8erf/b8erfc.json` (flush bisect + 0.5 crossing). Harness: `erf_map.py`,
`erf_cody.py`, `erf_fdlibm.py`, `erf_boost.py`.

## erf coefficient-recovery outcome (2026-07-17 session) — THERE ARE NO COEFFICIENTS

The "custom Microsoft rational tables" hypothesis DISSOLVED. Findings, in order:

1. **All remaining published candidates ruled out** (agent sweep + direct races):
   Boost int_<64> tables, Cephes ndtr, Ooura gamerf derf, Hart 5666, SLATEC,
   renormalized Cody/Cephes variants, plus every constant/rational micro-form
   (multiply, divide, split-constant, Padé [m/n] m,n≤8, Taylor truncations,
   two-product sums — all swept over constant neighborhoods).
2. **The z<0.5 branch is the NSWC gratio a<1 DIRECT path (branch 190)** — the same
   TOMS-654 source as the gamma side, with a mis-transcription trap: for a=½,
   x=z²<0.25 always routes 190 (`ans = exp(a·ln x)·g·(0.5+(0.5−j))`), NEVER the
   complementary 200-path (whose 1−q staging is catastrophic at tiny z in ANY
   precision — proof by granularity).
3. **The mystery constant is g = 1 + gam1(½)** — the NSWC gam1 rational itself,
   evaluated in x87 EXTENDED: h = `0x3fc06eba8214db6c` (cf. fdlibm's efx
   `…db69` — 3 ulp apart), g ≈ true·(1+8.5e-17), matching the measured effective-
   constant center (+6.5e-17 ± wobble). The earlier "q0 = sqrt(π_double)/2 anchor"
   was this same value seen through a division-form lens (1/g quantization
   coincidence, 11/15 partial fit).
4. **x87-extended compilation required**: all-double staging gives ±8-ULP tiny-z
   wobble (ruled out); extended log/exp keeps the exp(0.5·ln x) round-trip
   sub-ULP as observed. NOTE the tension with the gamma-side a≥1 path 20, which
   PROVED double-rounded log staging (`sp_both`) — different call sites of the
   same compiled function can spill differently; treat per-branch.
5. **Best models**: true-x87 Rust race (`check_erf190.rs`, Ext80 fFEXP/fFLN,
   512 spill configs): 663/1218 on z<0.5 (misses ±1, one ±2); designed
   max-|δ(z²)| battery (`answers-b10.json`): z̃=z-direct×g wins 37/50 over
   sqrt/explog-of-RN53(z²) and reflection forms. ~92% of rows within ±1.
6. **Residual — now QUANTIFIED (2026-07-17 hunt session)**: the last staging op
   is a deterministic sawtooth measured at full resolution on 128-step mantissa
   ladders in two binades (`answers-b11.json`, m30: z≈2⁻³⁰; m20: z≈2⁻²⁰) via the
   true-x87 dump mode (`check_erf190 <dir> dump` → per-row model phase):
   ε(m) = rising ramp ≈ +0.145 ULP per 1/128-mantissa-step, cut by −0.85-ULP
   down-teeth whose frequency GROWS with mantissa (period ≈6 steps at m≈1.4,
   ≈2.4 at m≈1.9 → tooth-phase ∝ m³ᐧᐧ⁴), amplitude ×3 larger at m20 than m30.
   This is the beat of an x²-magnitude term against a fixed ~2⁻⁶⁴ quantum on a
   z²-scale accumulation — i.e. the series/j/inner cluster in an arrangement
   OUTSIDE the tried parametrization (13 axes enumerated and ruled out at the
   850/1508 plateau: zz/series/j/zl/gam1-eval/gam1-ret/g/w/inner spills,
   association orders, GRAT1 pass-r, closed z-direct/sqrt/explog forms — b10
   designed max-residue battery pins z̃ as z-direct 37/50). Next probe: derive
   the exact tooth-position law from the dump (teeth are bit-precisely located),
   fit candidate quantized-accumulation generators analytically (sum⊕t at 64-bit,
   inner-poly x-term phases, alternative j-series arrangements incl. the Excel
   variant possibly fusing (1−j)), and verify against the m20 tooth set before
   any spill re-enumeration. Data: `answers-b9train.json` (1190),
   `answers-b9heldout.json` (256, UNTOUCHED — promotion gate), `answers-b10.json`
   (50), `answers-b11.json` (256 ladder), `answers-b11c.json` (511 erfc
   complement view, unanalyzed — pair-decoding reserve), `dump-m30.txt`.

## erf tooth-law measurements (2026-07-17 second hunt session) — bit-precise phenomenology

The last-op sawtooth was measured to bit precision via oracle-driven batched
bisection (`tooth_bisect.py`, 16-point rounds, ~16× bracket shrink/round;
`tooth_positions.json`). Facts any candidate mechanism MUST reproduce:

1. **Teeth are steps in Excel-vs-true-chain-model ε**, −0.85 ULP each, ramp
   +0.145 ULP per 1/128-mantissa step between teeth (z≈2⁻³⁰ binade).
2. **Linear in z, constant period within a binade, near-zero-anchored**: 11+
   consecutive teeth at exactly equal Δz; two teeth bisected to ~2⁻⁶⁶-relative:
   t1 = 1.13327213842e-9, t2 = 1.52563759794e-9 = t1 + EXACTLY 9 periods →
   **p(e=−30) = 4.35961621689e-11** (= 2.996·2⁻³⁶, NOT exactly 3·2⁻³⁶);
   t/p ≡ 0.995 (mod 1) — grid anchored ~at zero.
3. **Regime transitions**: half-quantum grid slip at m = 1.5 exactly; spacing
   collapse ≈3× after V crosses its binade (m = 2/g ≈ 1.7724).
4. **Cross-binade nesting**: at e=−40 BOTH a coarse (~6e-14) and a fine
   (5.949e-17/k, k∈{1,2} unresolved — bad bracket) structure exist; periods are
   NOT a smooth function of e (apparent log-slope ≈1.95 between −40/−30 but the
   law breaks at −25/−15). Multi-scale/nested sawtooths.
5. **Amplitude law: ε_amp·|zl| ≈ 25.7 ULP constant** across binades
   (0.93@|zl|=27.7, 1.48@17.3) ⟺ constant-absolute perturbation of zl²/2 —
   no computed quantity matches yet.
6. **Q-side**: ERFC ≡ RN53(1 − P-internal) at the tooth zone (48/48) — the
   generator is P-side/pre-complement; the complement is double-staged.
7. Ruled out structurally: all log-spaced generators (exp/ln tables, F2XM1
   boundaries, zl-grids — teeth are z-linear), x-quantized generators
   (1/m-spacing contradicts the exact arithmetic tooth progression), decimal
   round-trips, w-quantization (amplitude would be enormous), single/double/
   split-constant forms, and 1024 spill/association configs of the 190-path
   with true x87 chains (plateau 850/1508).

**Continuation plan**: (a) resolve p(−40) k-ambiguity with a fine scan
IMMEDIATELY after t4 (the t5 bracket excluded the first ~5e-17); (b) bisect
neighbor-teeth at e=−15 (t8 = 3.70029939053e-5 done) and e=−25 (t6 bisection
stalled — teeth shallower there); (c) fit m30's full 128-point ε as
ramp+sawtooth and examine the residual for the second generator; (d) test
generators whose PHASE is z-linear but AMPLITUDE is ulp-scale (beat/modulation
constructions); (e) the b11c erfc complement mid-range pair-decoding remains
unanalyzed. All captures cached; batched-bisection machinery reusable.

## Multi-agent closure sweep (2026-07-17 session 3) — five parallel verdicts

1. **BETA SIDE CONFIRMED = BRATIO (TOMS 708)** (`agentA_bratio.py`, full dependency
   tree transcribed): argument stagings pinned — wrappers pass the ACCURATE
   complement (`FDIST: x=d2/den, y=d1*F/den`; `TDIST: x=df/den, y=t²/den`, one-tail
   = 0.5·two-tail bit-exact). Decisive branch-differential: **bpser in plain double
   BEATS correctly-rounded betainc on FDIST/TDIST** (11/6, 5/3, 8/4) — literal code
   identity; F.DIST.RT bpser 5/5. **bgrat (a≫b tail) is the Excel-custom/extended
   sub-kernel** (double 2/12 vs CR 8/12) — the beta-side erf-analog. bpser's ±1-2
   residual = the x87 EXP/LN signature. Branch battery for bgrat: `answers-b15.json`
   (126 rows, cached).
2. **Taylor staging CORRECTED + normalizer MEASURED** (`agentB_*`): Excel sums the
   series FORWARD with 1/a as an OUTER factor (28/45 vs wk-backward 16/45 at a=2);
   normalizer = divG with **G = CR-double Γ(a) ±1 ULP ≡ exp(internal GAMMALN)** —
   NOT NSWC gamma (+22..33, score 0), NOT worksheet GAMMA(a). At a=2, EVERY miss
   resolves within ±1 ULP of exp(t1) with zero series changes — the residual is
   Excel's ≤-nearest-rounding exp (x87 CRT, one-sided). Feeds G3-02: the internal
   lgamma at fractional a is pinned to exp⁻¹(CR-Γ ±1).
3. ***INV = CONVERGED ROOTS** (`agentC_*`): DCDFLIB gaminv's early-stop schedule
   RULED OUT (worst of three models); Excel publishes fully-converged near-CR roots
   of its OWN forward (Excel-vs-CR scatter = conditioning-amplified last-bit forward
   rounding, κ-correlation 0.968/0.995). The *INV lane needs no schedule archaeology:
   ported forward + converge-to-last-bit inverter.
4. **erf sawtooth decomposition** (`agentD_*`): single z-linear sawtooth (NOT two
   superposed) threads 100% of the m<1.5 publish intervals (A=0.855±0.008,
   p=3/64 exactly, uniform teeth); past the V-binade the SAME generator's period
   collapses to ≈P/3.5; second generator = a slow BEAT ENVELOPE (weak at m30,
   strong at m20, lag-1 autocorr +0.89 sub-publish). Near-1-constant-multiply
   forms RULED OUT by the noise-free equal-period argument; the generator is a
   z-linear beat with slope-difference ≈2⁻⁴⁷·⁶ (≈21 ULP of g) or a 2⁻⁶⁴-quantum
   accumulation at z-scale. Still unidentified; comb structure at e=−40/−15
   (`answers-b14.json`) consistent with the beat picture.
5. **GRATIO PORTED TO OXFUNC** (merged c71cde5 + corrections fa275e0):
   regularized_gamma_p/q now run the identified kernel with the Excel-variant
   deviations (no a=0.5 erf dispatch; erfc1 via depth-1 recursion) + the agent-B
   staging/normalizer. Corpus: CHIDIST 12→**144**/195 exact (max overflow-class→52),
   GAMMA.DIST 64→**137**/268 (max 38→21). 1507 lib tests green, no pins changed.

## x87-exp last mile (2026-07-17 session 4) — the kernel exp is a STATIC LEGACY CRT

Racing the corrected staging with real chains (`check_gratio_x87.rs`) and ctypes
DLLs settled the exp identity question by elimination:
- **x87 worksheet chain (fFEXP/fFLN) REFUTED for the kernel**: RN53 of the
  64-bit chain ≈ CR at double granularity — all four exp/log combos score
  IDENTICALLY on 516 rows; it cannot produce the one-sided ~38% miss rate.
- **Modern UCRT exp/log ≈ CR** (25/45 = the CR score) — not Excel's.
- **msvcrt / msvcr100 / 110 / 120 as loadable on this host: all 25/45** (they
  forward to near-CR code on modern Windows) — not Excel's.
- **fdlibm e_exp remains the best public proxy (28/45)** — its rounds-low bias
  partially matches. Agent-B's decode stands: every a=2 miss is exactly a
  ∓1-ULP exp(t1) deviation, Excel's exp ≤ nearest (one-sided low).

CONCLUSION: the kernel exp is the 2010-era CRT exp STATICALLY LINKED inside
Excel's binaries (the same pattern as the statically-linked C pow identified in
the bond lanes) — an Intel-style table-based SSE2 exp with ~0.5-1 ULP one-sided
error. Recovery paths: (a) transcribe the msvcr100-era x64 exp op-graph from a
period binary; (b) treat the remaining per-row exp deviations as a measured
±1-ULP table (they are fully determined by the corpus: implied exp(t1) bits are
recoverable per row). The Cephes-igam-form series staging (ans from 1.0,
c/ans <= MACHEP stop, ·ax/a publication) is confirmed as the exact series form.


## bgrat verdict (2026-07-17 session 4, agent F) — tail region is an op-graph wall

Branch census on the fresh b15 battery (126 rows): bpser 59, bup_bpser 37,
bgrat 14, bpser_sym 9, bfrac 4, bup_bgrat 3. Findings:
- **Excel's beta TAIL region (bgrat + bup composites) tracks correctly-rounded
  betainc far better than NSWC-double** (CRc complement-form 12/20 vs 6/20 on
  pure-bgrat rows; bup_bpser CR 36/61 vs double 28/61) while PRESERVING the
  NSWC `0.5+(0.5-w1)` reconstruction — but it is NOT vanilla NSWC bgrat at any
  precision (every precision/eps/term-cap axis inert at 11/31), NOT the
  Excel-variant grat1 wiring, NOT NR-betacf (3/27), and not exactly CR either:
  structured ±4..±7 residuals persist at large-a/small-b and deep tails
  (bfrac rows to −35 vs CR — Excel's own tail carries real relative error).
  Extended precision DEGRADES the large-a rows: the residual is asymptotic
  truncation/formulation error, so Excel's tail is a DIFFERENT expansion —
  the same op-graph-wall class as GAMMALN-core; closure needs the binary's
  routine, not more fitting.
- **Honest held-out caveat**: the bpser beats-CR signature reproduces on the
  F-surfaces (11/12-vs-6/12, 5/5-vs-3/5) but NOT on the deliberately
  boundary-straddling b15 stress battery (30/59 vs 32/59 tied). bpser ==
  NSWC-in-double stands on well-conditioned surfaces; deep-tail rows drift.
- **Gamma-side a<1 wiring VALIDATED**: Excel-variant grat1 (no a==0.5
  dispatch) at prec-64/x87 scores 26/37 on the GAMMA.DIST a<1 rows with ALL
  remaining misses collapsed to ±1 ULP (at a=0.5) — the a<1 path is closed
  to the ±1 level under the extended model.


## Bulk oracle engine + mass tooth sweep (2026-07-17 session 5)

**Run-W109BulkBatch.ps1 landed**: recalc-sheet bulk capture, same ProbeBatch CLI
and shared OracleCache, validated 100.000% bit-identical on 1,831 gate rows
(ERF.PRECISE/CHIDIST/GAMMA.DIST) and byte-identical cache records. Throughput:
**8,800 probes/s** Excel-compute (~400x the per-batch-startup baseline); 114,688
ERF.PRECISE probes captured in 67s wall (`batch/answers-b16.json`). Invariants
preserved: scalar-cell path, args via Value2 references only (never decimal
formula text), Formula2R1C1 for dotted names.

**Mass tooth sweep** (16k-step ladders per binade + two zoom windows,
`dump-b16.txt` via the generalized check_erf190 dump): the erf last-op comb has
EXACT near-dyadic per-binade periods with wildly non-monotonic density —
p(2^-20) = 2^-33 exactly, p(2^-15) = 3*2^-29 exactly, e=-25 nearly quiet
(7 teeth/16k vs 5,960 at e=-20), amplitudes 0.75-1.5 ULP; the bisected
p(2^-30) = 2.996*2^-36 stays the one non-dyadic reading (continuous
measurement vs grid-quantized). No smooth or single-table generator law fits;
the structure suggests dependence on z's leading mantissa bits with
binade-dependent index width. Next: grid-free continuous period measurement
per binade (bisection pairs, now cheap), and correlate tooth positions
against leading-bit tables of z, w, and x simultaneously.


## Fine-comb measurement (2026-07-17 session 5b) — envelope aliasing exposed, bit-grids refuted

Dense per-binade scans at ~p/1000 resolution (81,920 probes in 20s via the bulk
engine, `answers-b17.json`/`dump-b17.txt`) show the ladder-scale "periods" were
ALIASED ENVELOPES: the true primary comb is ~1000x finer (e=-30: p = 4.30e-14
not 4.36e-11; e=-20: 5.42e-14; e=-15: 3.14e-12; e=-25: 1.67e-12; e=-40:
1.04e-20), with tooth amplitudes still 0.55+ ULP. The fine periods are
NON-dyadic (0.757-0.954 x 2^k) and the anchor-integrality test against z-bit,
3z-bit, w-bit and x-bit grids returns mean|frac| = 0.25 = the uniform-random
baseline over 16k+ teeth: **ALL leading-mantissa-bit-table generators are
REFUTED**. The earlier bisected p(2^-30) = 4.36e-11 and the m30 3/64-grid
teeth were beat-envelope structure of this fine comb (explaining their exact
9-period consistency: bisection tracked the envelope, which is real but
secondary). Relative fine-periods are wildly non-monotonic across binades
(7.9e-8, 4.5e-8, 4.6e-5, 3.6e-5, 9.4e-9 at e=-15..-40).

IMMEDIATE next step (cheap, no captures): re-dump the same answers under a
DIFFERENT model config (toggle w_dbl / zz_dbl) and compare tooth positions -
model-side teeth move or vanish, Excel-side teeth are invariant; this
partitions the fine comb between Excel's generator and residual model-side
staging before any further theory.


## Config re-dump partition (2026-07-17 session 5c) — the fine comb IS Excel-side

Differential dumps of the same 82k answers under three model configs (base 304,
w_dbl 432, zz_dbl 305; `dump-b17-{base,wdbl,zzdbl}.txt`):
- **w_dbl toggle: ZERO effect** in every binade (tooth sets identical) — the
  w-spill axis is irrelevant to the comb.
- **zz_dbl toggle: e=-15/-20/-30 tooth sets 100% invariant** => the fine comb
  there is EXCEL'S GENERATOR, not model staging. At e=-25 ~30% of base teeth
  were model-side (5713 -> invariant subset ~4006) and at e=-40 the zz_dbl
  config ADDS ~2000 artifact teeth (base's 1093 all survive => base is clean).
- Consequence: the base-config fine-period table stands for -15/-20/-30/-40;
  re-derive e=-25 from the invariant subset. Part of the cross-binade
  non-monotonicity was model contamination at -25.

The Excel-side fine comb (non-dyadic periods, no bit-grid anchoring, dense at
0.55+-ULP amplitude) is now the confirmed, isolated target for the erf last-op
generator hunt.

## Open sub-identifications (recipes)
2. **Internal Γ normalizer**: with the gratio structure pinned, solve per-a for the
   normalizer double that bit-matches each fractional-a slice (interval intersection
   over ~20 x-points each — the slice over-determines it); compare against published
   GAMMA bits, CR-Γ, exp(published GAMMALN), and G3-02's custom-rational hypotheses.
   This is a new measurement window into the G3-02 wall.
3. **Taylor micro-staging**: enumerate on the a=2 slice (Γ=1 exact, gln=0 exact,
   47/80): term-recurrence staging, sum/publish orders, exp/log model per-op. Then a=6.
4. **CF fine detail** (fractional a, x ≥ 1.1 route, and the smalla-series j/rexp
   staging at a<1) — after 1-3.
5. **Beta side = BRATIO (TOMS 708)** — same library, same era: capture BETA.DIST
   discriminating batteries (bpser/bfrac/bgrat branch probes), transcribe bratio.f,
   race. FDIST/TDIST then need only their argument-transform staging.
6. **Wrapper details**: a==1 P-form on x>1 (expm1 vs 1−exp Q-primary — 12 residual
   ±1 rows in (1,3)); CHIDIST df=2/GAMMA.DIST consistency on the Q side.

## Files

- `gen_batteries.py`, `analyze.py` — B1-B4 design + deviation map (829 probes)
- `batch-b5.json`/`answers-b5.json` — integer-dispatch/fractional-a discriminators (207)
- `emulator.py` (mpmath staged models), `check_igamma.rs` (true-x87 Ext80 race —
  ruled the extended family out at stage A)
- `implied_arg.py`, `arg_fit.py`, `sum_decode.py`, `staging_fit.py` — residual decoders
- `cdflib_py.py` (faithful GRATIO + gam1/rlog/rexp/erf/erfc1/gamma_nswc transcription,
  injectable LOG/EXP/GAMMA_FN), `gratio_race.py`, `gratio_detail.py`
- `erf_map.py`, `erf_cody.py`, `answers-erfp/erfcp.json` — the erf sub-lane
- `cdflib/*.f` — the fetched TOMS 654 Fortran sources

## Method notes (durable)

- **Multi-view exact-transform probing** (CHIDIST(2x,2a) vs GAMMA.DIST(x,a,1) vs
  GAMMA.DIST(2x,a,2)) collapses 12 surfaces to one kernel measurement and isolates
  per-function staging for free.
- **Implied-argument decode**: for kernels shaped `sum·exp(arg)`, tiny-x rows make
  `arg_implied = ln(P_excel/sum_true)` measurable to ~2⁻⁵³ absolute; comparing against
  exact rounding residues of candidate stagings identifies WHERE the double-roundings
  sit, one op at a time. The ×a amplification of the ln-residue was the smoking gun.
- **Dispatch discovery by contradiction**: when one op-graph cannot explain two slices
  of the same code path, suspect an argument-value dispatch (a==1 here; the near-integer
  probe a=1+2⁻²⁰ is the cheap decisive test).
- **Branch-differential scoring**: with a multi-branch reference implementation,
  per-branch match rates (91% / 48% / 25%) localize which subroutines are shared vs
  Excel-custom far faster than whole-function scores.

## b18 matched-resolution scans (2026-07-17 session 5) — the "fine comb" was ALIASING; phase-gradient is the real fingerprint

Battery b18 (242,474 ERF.PRECISE rows, bulk engine): every binade scanned at
THREE matched relative step scales (2e-8 / 2e-9 / 2e-10), anchored at the b17
windows. Result, uniform across all five binades:

- **No resolved comb exists at any scale.** The "median gap" is always 2-5 GRID
  steps at every scale — it rescales x10 whenever the grid does (e.g. s25:
  8.0e-8 -> 8.0e-9 -> 8.0e-10 rel across the m/f/u scans). Every fine-period
  previously tabulated from dense scans (6.4e-8 / 4.4e-8 / 5.6e-5 / 3.2e-5 /
  6.8e-9, and their non-monotonicity) was an ALIASING ARTIFACT of the scan
  grid. The b17 "config re-dump partition" tooth sets remain valid as
  point-sets, but their gap statistics carry no period information.
  METHOD CAUTION (durable): a period estimated from a dense scan is only real
  if it is reproduced at a 10x finer grid; otherwise it is the grid echoing
  its own step through the miss density.
- **The real structure is the phase gradient.** Using the model's extended
  value position within its ULP (phase), miss probability rises monotonically
  toward the rounding boundary:
    e=-25/-30/-40: P(miss) ~ 10% at phase 0 -> ~48% at |phase|=0.5 (identical
                   profiles across all three binades);
    e=-15/-20:     ~36% -> ~52% (much flatter = larger perturbations).
  Misses at phase~0 exist, so the driver reaches >=0.5-1 ULP; the equidistributed,
  spatially-incoherent pattern is the signature of per-row last-bit differences
  in an internal transcendental (exp/log op-graph), NOT a staging/association
  difference (those are spatially coherent). Envelope-scale density variation
  is real (s20 windows: 29-55% miss density).
- CONSEQUENCE: the erf last-op lane MERGES with the static-CRT-exp lane. The
  scoring instruments for candidate exp/log op-graphs are (a) exact-match rate
  on b18 (242k rows), (b) the per-binade phase-gradient profile, (c) the 45-pt
  implied-exp corpus. Period-matching is dead.

Files: batch-b18.json / answers-b18.json / dump-b18-base.txt / analyze_b18.py /
period_rederive.py / excel_side_period_table.json (superseded by this section).

## *INV converged-root landing (2026-07-17 session 5)

Landed in production (validated on the b14 corpora, held-out b19 captured
separately):

- `bisect_inverse` (special_math_common.rs): early-stop 4*EPS bisection
  replaced by FLOAT-LATTICE bisection to adjacent doubles, publish hi
  (f(lo) < p <= f(hi)); order-preserving i64 key + i128 midpoint, sign-safe.
  b14 effect: GAMMA.INV 8->18/60 exact, worst +880,380 -> -16 ULP;
  BETAINV 2->4/30, worst +1,910,580 -> +13 ULP (residual = the pre-BRATIO
  beta forward, a separate lane); publication-rule race: hi 18/60 vs
  closest 17/60 vs lo 7/60 (gamma side) — hi retained.
- `chisq_inv_rt_kernel` (chi_f_t_family.rs): CHIINV now inverts the PUBLISHED
  right-tail surface Q directly (negated-forward convention) instead of P at
  1-p. The 1-p staging carries a systematic -5..-33 ULP bias (rounding loss in
  1-p); Q-direct: 10->16/60 exact, residuals collapse to +-1..5 (worst -91 at
  one deep-tail row).
- `gamma_inv_kernel`: upper bracket now extends by doubling until
  f(hi) >= p (lattice invariant).
- Racer: `check_inv.rs` (calc_graph_racer) — races early-stop vs lattice
  {hi, lo, closest} x staging spaces on the b14 corpora. GAMMA.INV x-space vs
  z-space indistinguishable at beta=1 (all b14 gamma rows); b19 includes
  beta != 1 discriminator rows + FINV/TINV probes of the same
  invert-published-surface principle.

Full oxfunc_core suite green (16 test binaries) after the change.

## CHOPPED-EXP IDENTIFICATION (2026-07-17 session 5) — the kernel's series exp is TRUNCATED toward zero

The decisive break in the "static legacy CRT exp" wall came in two steps:

1. **Real-binary CRT sweep (agent G) closed the entire Microsoft hypothesis
   space.** A 32-bit harness called exp() in the genuine DLLs — msvcr90
   9.0.30729 (the exact Office-2010 CRT generation, loaded via a VC90 SxS
   activation-context manifest), msvcr100 (2010-03-18 binary), 110, 120,
   msvcrt — plus the x87 fallback path (_set_SSE2_enable(0)) and bit-faithful
   transcriptions of the AMD K8 32-entry and x64 64-entry table exps
   (ReactOS libm_sse2 exp.asm == Open64 libacml_mv, AMD provenance pinned).
   ALL REFUTED: the 32-bit SSE2 CRT exp is one Intel-lineage __libm_sse2_exp
   rounding one-sided HIGH (0..+1 vs CR) — the mirror image of Excel; x87 and
   x64-AMD are CR-identical on the corpus. Best public proxy stays fdlibm
   28/45. Excel's exp is in {CR, CR-1}, one-sided LOW, CR-1 on 20/45 rows.
2. **20/45 = 44% ~ half is the truncation signature**: CR-1 exactly when CR
   rounded up. floor(true exp) scores **38/45** (vs CR 25, fdlibm 28) —
   rd_exp and RN64-then-RZ53 agree on all 45 args. The one-sided-low
   "rounds-low CRT exp" story was a truncated PUBLICATION all along; the
   earlier x87-chain refutation had only raced nearest publication.

**Call-site localization** (full 692-row corpora, emulator + replica races):
the chop lives ONLY at the gser series r = exp(t1)/G call site.
- a==1 wrapper rows LOSE under chop (its exp/expm1 are nearest);
- continued-fraction rows LOSE (cf/P 10 lost, 0 gained);
- a<1 (190/200-path) rows LOSE;
- a>=1 series rows GAIN: production-staging replica 148->174/306 training,
  b20 held-out (fresh a in {1.75,2.25,3.25,4.5,5.5,8,12}, df-truncation
  corrected) 65->68/111, worst -22 -> -19. Fractional-a margins are capped by
  the normalizer (exp of internal lgamma, G3-02 lane), not by the exp.
Per-call-site rounding differences inside one compiled function are now a
PATTERN in this kernel (cf. the a>=1 double vs a<1 extended log staging).

**LANDED in production** (special_math_common.rs):
- `exp_rd(x)`: Tang-style 64-entry table exp in double-double (~2^-100),
  directed truncation before exact 2^m scaling; constants generated
  programmatically as bit patterns (a hand-converted table entry error was
  caught by regenerating — never hand-convert constant tables). Validated
  0 mismatches vs mpmath floor-exp on 25k points incl. the +-708/709 edge
  bands; |m|>1022 and the subnormal sliver fall back to nearest exp.
- statement-20/534 call sites now pass r_series = exp_rd(t1)/G to the series
  arm and r = exp(t1)/G to the CF/asymptotic arms.
- **a==1 dispatch landed inside gratio**: (P, Q) = (-expm1(-x), exp(-x))
  nearest (the identification's wrapper dispatch; a pinned CHIDIST(1,2)
  witness enforces it against the chop).
Corpus: CHIDIST 148 -> **152**/195, GAMMA.DIST 151 -> **159**/268 (from
12/195 and 64/268 pre-campaign). Full suite green (1604).

Remaining gamma-side residual: the internal approximation BEHIND the chop
(7/45 rows where Excel's pre-truncation value crosses a boundary that
floor(true) doesn't — an approximation with ~2^-56-ish error), the fractional-a
normalizer identity (G3-02), and the erf/beta sub-kernels. The erf 190-path
exp is NOT the chopped one (b18 phase evidence both-sided; a<1 rows lose
under chop) — the erf last-op hunt continues in the phase-gradient frame.

## *INV published-surface principle extended (b19 held-out)

b19 (fresh rows, never raced): CHIINV Q-direct CONFIRMED held-out (15/40 vs
6/40 for P at 1-p, same systematic negative bias on fresh rows). The same
invert-the-published-surface staging decisively improves FINV (0/32 -> 3/32,
small-p bias -60 -> +2) and TINV (residuals -4..-238 -> mostly +-1..7):
LANDED for f_inv_rt_kernel (roots f_dist_rt's accurate complement form) and
t_inv_2t_kernel (roots t_dist_2t's surface). GAMMA.INV z-space vs x-space:
+4 rows on 48 discriminators (beta=3) for z-space — a hint, below promotion
bar; x-space retained. BETAINV/CHISQ.INV inverter-limited no longer; forward
error dominates.

## Batteries added this session

- b18 (242,474 ERF.PRECISE rows): matched-relative-resolution scans; killed
  the period-table premise (see b18 section above).
- b19 (320 rows): held-out *INV + FINV/TINV staging probes.
- b20 (112 rows): held-out gamma series (fresh a); chopped-exp gate.
- b21 (127 BETA.DIST rows): beta-tail discriminator battery (agent-H spec:
  GRATIO-substitution vs Boost small-b-large-a series vs CR) — scoring in
  flight.

## Beta tail: family PROVEN, realization OPEN (b21, 2026-07-17 session 5)

The b21 discriminator battery (127 live BETA.DIST rows: deep tail a in
{16..200} x b in {0.05..0.95} x y=2^-k, plus fractional-a composites) settled
the beta-tail family question and left the exact realization open.

- **FAMILY PROVEN = DiDonato-Morris TOMS-708 Eq-9 bgrat expansion.** Decisive
  signature: at k=2, a=118/200, Excel sits +41..+63 ULP from the TRUE value
  yet within +-7 ULP of every Eq-9-family realization across 25 rows. A
  63-ULP co-deviation from truth tracked to +-7 across the family is intrinsic
  truncated-asymptotic method error, not rounding coincidence. NSWC driver +
  0.5+(0.5-w1) reconstruction retained; composites are NSWC bup-shaped (not
  Boost's ibeta_a_step: Boost off +6/+14/+22 there).
- **NO exact realization** among: NSWC-double grat1 (4/127, max 56),
  GRATIO-sub nearest/chopped-r/chopped-all (8-10/127, max 37), Boost 1.35-1.42
  (6/127 but best <=4-ULP where the asymptotic error dominates: k=2/3 median 3
  max 8), Cephes 2.8, AS 63, NR betacf, or any routing/cap/eps forcing.
- **Chopped-exp is INERT on the beta tail** (+1/+2 exact over nearest): the
  gamma-side truncation does NOT transfer to the beta r=a*exp(t1) site. The
  transcendental-model axis (cr vs x87) is also inert here.
- Term-cap unidentifiable: the j-series eps-converges in <20 terms; caps
  20..60 are bit-identical.
- Residual bounded/structured (+-30). Next-cycle axes (agent-H): the r/u/h
  PREFIX op-graph (Excel may normalize via its own gamma, not NSWC
  algdiv/gam1) and the inner Q(b,u) kernel's exact arithmetic.

**CRITICAL STATE FACT**: OxFunc production `regularized_beta`
(special_math_common.rs) is a **Numerical-Recipes Lentz continued fraction**,
NOT a BRATIO port. The entire BRATIO identification (bpser plain-double =
literal code identity beating CR on FDIST/TDIST; bup/bgrat/bfrac/basym
routing; accurate-complement stagings) lives only in the Python emulator
(agentA_bratio.py). So the beta side has had NO production landing analogous
to the gamma GRATIO port. **The clear next material win is porting BRATIO to
replace the NR continued fraction** — the bpser bulk (non-tail) region would
gain the same way CHIDIST/GAMMA.DIST did, while the bgrat tail stays the
identified-family-unresolved wall documented here. This is a kernel-scale
lane (bpser, bup, bgrat, bfrac, basym, algdiv, gam1, gamln, brcmp1), not a
drop-in; it should be its own task with its own held-out gate.

Files: agentH_b21.py, agentH_b21_analysis.py, agentH_b21_out.txt,
answers-b21-beta.json; earlier agentH_{routing,routing2,cephes,boost,
gratio_tail,as63,report}.py + agentH_src_* sources.

## BRATIO PORTED TO PRODUCTION (2026-07-17 session 6)

The identified BRATIO kernel is now the production incomplete beta. Port =
op-for-op Rust transcription of agentA_bratio.py (the identification-bearing
spec): full subroutine tree (~1,530 lines, bratio_-prefixed: esum/alnrel/
rlog1/gam1/gamln1/gamln/algdiv/bcorr/gsumln/betaln/erf_nswc/erfc1/rexp/psi/
fpser/apser/bpser/bup/brcomp/brcmp1/bfrac/bgrat/grat1/basym + 200-line
driver), `pub fn bratio(a,b,x,y) -> (w, w1)`; `regularized_beta` rewired onto
it (y = 1-x); the Numerical-Recipes continued fraction DELETED.

Verification chain:
- Bit-identity race vs the Python spec (LOG/EXP = C runtime): 22/22 branch
  spot-checks (agent) + **20,008/20,008 random+targeted points, 0 mismatches**
  (independent). The port IS the spec.
- Full suite green (1,604), no pins touched.
- Held-out gate b22 (671 fresh live rows, disjoint values): old NR kernel
  167/655 exact (worst +-145) -> BRATIO **285/655** (worst 126, one
  bgrat-wall row; FDIST worst +37 -> -15, TDIST worst +-88 -> +17).
  Per-row: 422 improved / 60 regressed, ALL regressions in the bgrat-wall
  region (where no raced realization matches Excel; the old kernel was
  accidentally close there).
- b21 deep-tail corpus: old **0/127, worst 8,848 ULP** -> new 4/127, worst
  56. The catastrophic tail class is eliminated.

ACCURATE-COMPLEMENT STAGINGS LANDED at the wrappers (the identified
argument passing): FDIST/F.DIST x=d2/den y=d1F/den (and cumulative mirror),
TDIST/T.DIST.RT/2T + t_cdf + TTEST x=df/den y=t^2/den; all F/T inverter
closures root the same staged forwards. b22 effect: TDIST 6->14/60 exact.
BETAINV/FINV/TINV inherit the better forward through the lattice inverter
automatically.

Open after the port: the bgrat-tail realization (family proven = Eq-9, exact
arithmetic unmatched — the +126 b22 worst-row lives here), the BETA.DIST
integer-shape fast path (binomial sum, bypasses BRATIO for integer a,b;
neither it nor BRATIO dominates vs Excel on the a=b=27 rows — probe later
whether Excel routes integers through bratio), and the A/B-bounds staging
for BETA.DIST ((B-x)/(B-A) accurate-complement hypothesis, unmeasured).
Baseline racer for old-kernel comparisons lived in a temp worktree
(OxFunc-preport, removed after gating); scorers: score_b22.py,
race_bratio_identity.py in the work dir.

## erf transfer-function verdict (2026-07-17 session 6, agent J) — the erf-path residual is DOUBLE-arithmetic scale

The b18 corpus is now a calibrated mass-verifier (agentJ_transfer.py: build/
gate/hyp/invert; 242k rows, 87s; linearized sensitivities validated 2004/2004
vs full-chain evaluation). Findings:

- ALL extended-precision primitive hypotheses REJECTED by ~2 orders of
  magnitude: CR-64/x87-64 exp or log differences predict 0.04-1.2% miss
  densities vs observed 25.6-43.7%.
- CHOP REFUTED on the a<1/erf path outright: both +1 and -1 flips in every
  binade (e.g. e=-40: 7,920 vs 4,684), positive shifts to +0.57 ULP.
- What the data demands: shift(z) = smooth per-binade bias B(z) (+0.065/
  +0.073/-0.099 ULP at e=-40/-30/-25; wandering +-0.5 ULP with ~1e-5
  coherence at e=-20) + a DETERMINISTIC per-argument residual delta(z) whose
  DISTRIBUTION over the sampled grids is uniform, total width 1.01
  published-ULP ~ 0.90 dbl-ULP of w, identical across binades to 0.3%.
  Forward-validated: densities AND gradients reproduced bin-by-bin.
  TERMINOLOGY (standing rule): this is NOT noise — delta(z) is reproducible
  signal (equidistributed high-frequency rounding residual of
  double-precision internal arithmetic). The distribution is a CLASS
  constraint that killed the extended-precision families; the per-row signed
  values are banked in agentJ_constraints.jsonl (79,510 rows) and remain the
  signal the exact op-graph must reproduce row-by-row.
- Structural point: w = exp(ln z) ~ z sits pinned to the double grid (mean
  |position| 0.002 dbl-ULP), so no publication-mode change of an ACCURATE exp
  can produce the misses — the internal routine itself carries double-scale
  error on this path.
- TENSION to resolve: the POISSON k=0 channel shows a much tighter profile
  (~99.4% exactly CR) — inconsistent with a +-0.45-ULP exp residual. b18
  cannot separate an exp-result-relative residual from an lnx-absolute one
  (S-ratio frozen in every b18 window). If the residual actually lives in
  the internal LN (a double-precision routine with ~+-0.5-0.7 ULP rounding
  residual), the internal EXP can be ONE tight near-CR routine at every site
  (chop-published at the series site, nearest elsewhere) — the clean
  unification.
- DISAMBIGUATION CAPTURED: battery b25 (163,840 ERF.PRECISE rows) scans the
  z-mantissa ~ 1.7724 crossing where ans crosses its binade (S_exp halves,
  S_log unchanged). If miss width in published ULPs halves across the
  crossing -> exp-relative; if not -> lnx-absolute.

Files: agentJ_transfer.py, agentJ_rows.npz, agentJ_constraints.jsonl (79,510
miss-row constraints), agentJ_summary.json, agentJ_{cfgtest,fit,fit2,blocks,
shape15}.py; batch/answers-b25-erfx.json.

## bgrat implied-prefix decode (2026-07-17 session 6, agent M) — normalizer is algdiv-class; b21 under-determined; b25 designed

Decoder gates passed (synthetic recovery 121/121; leakage control quantified
the prefix/series entanglement). On the 121 sharp direct-bgrat rows
(single-final-rounding: excel = RN(u*S), w=0, eps=1.5e-14, l=0):

- **"Normalize via own lgamma" RULED OUT HARD**: lgamma-difference prefix
  stagings deviate +-100..900 ULP at a=118-200 (exp-of-large-arg cancellation
  amplification); Excel's implied prefix stays within +-60 (mostly +-25) at
  all a. Excel's bgrat normalizer is CANCELLATION-FREE, algdiv-class. (One of
  the two open axes from the b21 verdict is closed.)
- x87 vs SSE2 on the prefix chain: bitwise-indistinguishable on b21 rows.
- Stop-position/eps variants: ruled out (flat race; implied S matches a
  ladder partial sum on only ~5/121 rows).
- Implied-q (inner kernel) decode is 0-1-ULP sharp but NO tested q-kernel
  matches (CRQ 2/102, GRATIO 4/102, grat1 7/102, wobble +-30; 19/121 rows
  admit no q at all under NSWC u) -> the remaining freedom is JOINTLY in the
  ladder per-term arithmetic and a (u,q) staging pair outside the tested
  families. b21 is provably under-determined for this split.
- **b25-bgrat battery designed** (batch-b25-bgrat.json, 822 rows,
  agentM_b25_meta.json): shared-z a-sweeps (a bit-walked so z lands on the
  SAME double per group) make the inner Q(b,z0) common-mode and read the
  normalizer staging as a dense-a curve; predicted separation >=3 ULP for
  lgd/1exp on ~800/822 rows and q-kernel variants on 558/822.

Files: agentM_decode.py/out, agentM_series.py/out, agentM_gen_b25.py.

## bgrat b25 analysis (2026-07-18, agent M) — op-graph wall confirmed; lane parked pending exp/ln identities

The 822-row shared-z discriminator settled what b21 could not, negatively and
precisely:

- **Group-intersection falsification**: all 120 (10 shared-z groups x 12
  op-graphs) common-q intersections are EMPTY, with per-group "no admissible
  q" rows — every tested realization (lnx {alnrel, CR, x87, log1p} x r
  {nswc, gamma-lane, exp/Gcr, pow-staged} x u {algdiv-exp, chop, x87,
  pow(nu,b)} x q {GRATIO, grat1, CR} x accumulation x 6 eps) is falsified AS
  A FAMILY, not mis-tuned. Forward race caps at ~8-9% everywhere.
- Stop-rule/eps artifacts excluded (required eps windows are empty).
- **Measured residual structure (per-row, banked)**: within groups the
  implied-q offsets are +-3 q-ULP base wobble PLUS bimodal ~10-ULP cluster
  flips, a-interleaved (not monotone — not a series-depth threshold);
  deep-series k=2,3 rows carry +-30..103-ULP shared+differential series
  components. Normalizer: algdiv-CLASS stands (cancellation-free proven);
  exact member open. q*: GRATIO-neighborhood (-3..+15) but never
  consistently in-interval.
- VERDICT: the realization is outside the entire parametrized family — the
  wall is the INTERACTION of u-chain and per-term arithmetic. Same class as
  the GAMMALN-core/PMT precedents.
- PARKED with next-probe design banked (agent M): (i) differential z-pairs
  (same (a,b), z +-1-2 ULP) to read Excel's dQ/dz transfer and de-entangle
  q from u; (ii) bracketing rows at the observed cluster-flip a-positions to
  localize the discrete mechanism; (iii) b->1- sweep collapsing r-staging
  differences. RESUME CONDITION: revisit when the internal exp/ln op-graphs
  land (the u-chain is composed of them; their identities may collapse the
  +-2-3-ULP wobble and leave only the flip mechanism).

Files: agentM_b25{,b,c,d}.py/_out.txt (per-row curves banked in
agentM_b25_out.txt A2/B2/C).

## Primitive-recovery campaign results (2026-07-18, agents I/N/J b23/b24/b25) — the primitive map

**INTERNAL LOG = CORRECTLY ROUNDED (RN53), bit-for-bit.** Proven two ways:
LOGNORM candidate-matched decode (b24: 2,151 RN-exact rows all delta 0; 849
interval rows all contain 0; zero routing surprises; BINOM residue slope AND
intercept 0.0000 ULP to n=720; WEIBULL residue 0+-0.003) and the b23A
cross-view solve (L == cr_log within +-1 ULP ~94.5%, exact 76.5%).

**INTERNAL EXP = ONE near-CR routine; publication varies by site.**
- Direct read (POISSON k=0, 30k rows): 99.490% == RN(CR), 0.457% CR-1,
  0.053% CR+1 — BIAS-LOW; off-CR density scales with |arg| (0% below 0.1 ->
  4.68% at ~100: reduction-step-count signature). pdf-site (EXPON pdf) is
  BIT-IDENTICAL to it 10,000/10,000 (one routine, nearest-published).
- Series site: the SAME near-CR value chop-published (unification not
  contradicted; small-|t1| channels agree ~57-65% within 1 ULP; large-|t1|
  gamma reads are actually LOG measurements — CR-log's +-1 ULP amplified by
  |t1|).
- Breakpoint scan (b23B): clean cells at small |t1|, spacing ~ln2/2^5..2^7
  (32-128-entry reduction table class).
- erf-190 path (b25 split, agent J): the residual is EXP-RESULT-RELATIVE
  (decisive m-transfer diagnostic: widths at b18 values to 0.1-3.4% where
  ln-attribution predicted +43%): equidistributed spread of width 0.90
  dbl-ULP + a SMOOTH deterministic per-argument bias, m-independent at
  e=-25/-30/-40, bias exp-frame (halves with width at the ans crossing).
  Structure constraints: e=-30 and e=-40 bias profiles IDENTICAL (corr
  0.9989-1.000, shared amplitude 0.0246 ULP) yet e=-25/-20/-15 mutually
  decorrelated; all table-cell foldings null at j=4..8 granularities.
  TENSION: 0.90-ULP width is inconsistent with the tight wrapper profile —
  either a second exp realization on this path, or a staging effect
  (e.g. pow-composition); op-graph lane must resolve.

**EXPM1 IS A SEPARATE PRIMITIVE** (EXPON cdf = -expm1(-x) definitively;
+-1-ULP ~symmetric, ~20% off-CR — less accurate than exp, NOT exp-derived).
GAMMA.DIST a=1 wrapper bit-identical to it (shared rows).

**POW (distribution kernel) = exp(y*ln x) COMPOSITION** (b24: BINOM 100%
incl. exp+-1 tail; WEIBULL powf 797/800 vs binexp ~411/800; pow(x,1) != x on
605/800 — no exponent-1 shortcut). DISTINCT from the bond-lane binexp pow.

**INTERNAL LGAMMA = EXTENDED precision, sub-ULP from CR** (b24 GAMMA-window
reads: means +0.05/+0.007/+0.13 ULP, E_g nearest; double-grid inversion
fails 78% = extended signal; no separate integer fast path — RN(exp(CR
lgamma(n))) hits (n-1)! anyway). Distinct from published GAMMALN (the Cody
re-fit).

**OPEN / FOLLOW-UPS**: (1) series-staging reconciliation — agent I's a=4
decode prefers backward-wk + gamma_nswc over the landed Cephes-form +
(a-1)!; production implications to be raced per-a on the b23A corpus;
(2) poisson pmf staging (direct-product route proven; ~21% unexplained at
k=1 — a broader-error exp-site candidate); (3) the exp op-graph itself —
the 153 POISSON off-CR rows + b25 bias profiles are the fingerprint.

Maps banked: agentI_{poisson,expon,exp}_map.jsonl, agentN_{ln,lgamma}_map
.jsonl, agentJ_b25_residuals.jsonl (+ npz/summaries). Decoder gates all
passed (synthetic recovery exact).

## INTERNAL EXP IDENTIFIED (2026-07-18, agent O) — the x87 F2XM1 chain, dual-published

**Identity: x87 80-bit extended exp = 2^(x*log2e) with the NAIVE y - round(y)
reduction feeding F2XM1 (PC=64, RC=nearest), published RN53 at wrapper/pdf
sites and RZ53 (chop) at the gamma-series site. expm1 = the SAME F2XM1
primitive staged -expm1(-x).**

Evidence chain:
- POISSON fingerprint (30k rows): x87-f2xm1-naive reproduces the off-CR set
  **153/153 EXACTLY** (29,997/30,000 overall, 3 false-positives). Decisive
  structure-vs-precision control: RN64(true)->RN53 — the same 64-bit
  precision WITHOUT the f2xm1 op-graph — reproduces only 1/153. Removing the
  y-round(y) cancellation (ln2-reduction variant) drops to 13/153: **the
  reduction cancellation IS the growth-with-|arg| mechanism.** LOG2E_64
  bit-exact with the fldl2e constant 0xB8AA3B295C17F0BC. AMD K8/64 tables,
  fdlibm, cephes: refuted (6-13/153, noisy).
- Chop channel (45-row corpus): x87-f2xm1 RZ53 = 38/45, bit-identical to
  floor(true) incl. the same 7 misses; RN53 scores 17/45 — the dual
  RN53/RZ53 publication model validated.
- expm1 (10k): -expm1(-x) staging confirmed (80.3% vs 30.5% for 1-exp); the
  ~20% symmetric +-1 residual is the raw hardware F2XM1 error curve.
- erf-path resolution: ONE op-graph, TWO argument deliveries — wrapper sites
  get a rounded-double argument (tight profile); the erf 190-path delivers an
  80-BIT EXTENDED zl to the same routine (the 0.90-ULP width + smooth
  bias(m)). No second realization needed.
- Residual (3/30,000 + the expm1 off-CR rows): the idealized RN64(2^f - 1)
  model double-rounds where the ACTUAL F2XM1 microcode rounds correctly —
  proprietary microcode, NOT clean-room derivable from published sources,
  BUT this host already renders bit-exact F2XM1 via inline x87 asm
  (crate::excel_numeric::x87) — hardware-chain verification is the closure
  test and is behaviorally clean (executing the instruction = black-box).

RECONCILIATION: the "stats rewrite is plain SSE2 double" verdict stands for
the KERNEL ARITHMETIC; its transcendental PRIMITIVES are the x87 hardware
chain — rejoining the project-wide "Excel transcendentals are x87" prior.
The session-4 "x87 chain == CR at double granularity, refuted" verdict was an
RN53-on-516-rows artifact: near-CR indeed, distinguishable only on the rare
fingerprint rows this campaign isolated.

Files: agentO_x87exp.py, agentO_race_x87.py, agentO_race_dr.py,
agentO_chop_validate.py, agentO_expm1.py, agentO_verdict.json (+ support).
NEXT: hardware-chain verification races (real F2XM1 via inline asm) on all
channels; then production landing design (exp sites -> x87 chain with per-site
RN53/RZ53 publication; expm1 -> f2xm1 staging; erf190 with extended delivery).

## PRODUCTION LANDING: the F2XM1 chain everywhere (2026-07-18, commit 223cfa5)

- Hardware verification first: RN53(real chain) = 30,000/30,000 on the
  POISSON channel; RZ53(real chain) = 38/45 on the chop corpus with the same
  7 misses as floor(true) — those 7 are series micro-staging (x87-ln53 == CR
  on all 45 rows; extended-t1 delivery REFUTED for the series site, 16-20/45
  with +-17 misses).
- Landed: excel_exp_rz (chain + RC=chop store; dd floor as portable
  fallback); ALL 49 exp sites in gratio/bratio/erf switched to excel_exp;
  POISSON pmf exp switched (k=0 rows now carry the proven behavior).
- Gates: suite 1,606 green; gratio corpus stable (152/195, 159/268); b22
  stable (285/655); **b14 BETAINV 4 -> 12/30, worst +13 -> +5** (chain exp
  through the beta forward).
- bgrat re-race WITH true primitives (agent M): the wall stands — the body
  op-graph itself (53-bit, per-op-DR, and register-resident families ALL
  falsified by group-intersection); banked constraints: extended-body > DR >
  plain-53; GRATIO-sub q > grat1 in all 12 combos; next probes designed
  (differential z-pairs, flip bracketing, b->1- sweep). Parked.
- GAMMALN kernel landed same commit (see the G3-02 note): held-out 79.0%
  worst 5, from 0/79 worst 1,370.

Remaining to bit-closure on this cluster: gamma-series micro-staging (7/45
class + agentI summ divergence + the a=4 wk-question), expm1 staging, POISSON
product-route staging, erf staging race (agent J in flight), GAMMALN b1/b2
coefficients, bgrat body op-graph.

## erf staging race (2026-07-18, agent J) — 64.2% -> 66.3%; blocked on sub-ULP effective-g; refit round in flight

With the chain fixed, 14 single-axis staging variants + PC53 composites raced
against the b25 bias profiles:
- j-pipeline RN53 parks (C10-class) capture GENUINE e=-25 coherent structure
  (35.3% -> 58.6-65.8% there; sawtooth in j*2^53 frozen at e=-30/-40,
  equidistributed at e=-15/-20 — matching the measured class) but fine-scale
  phases partly wrong at e=-15/-20. Best composite C10 = 66.28% overall
  (baseline 64.18%).
- The universal 1.01-ULP width component is PARK-SHAPED (grid ~ 2^Ez), and
  C7's park perturbation correlates ~0.5 with the true residual at e=-30/-40
  — exactly the signature of a correct park with g known only to ~2^-53.
  V4 (park g*inner) refuted by a sign-flip tie; V12 (park g) refuted (+0.69
  vs measured +0.08); null axes: V6/V9/V10/V13.
- Verdict: not closed; b9heldout UNTOUCHED (training not decisive).
  NEXT (in flight): refit Excel's effective g at sub-2^-53 resolution via
  park-phase alignment on the clean e=-30/-40 profiles, re-race the
  composites; held-out only if decisive.

## erf lane PARKED (2026-07-18, g-refit round) — resting state banked

The effective-g refit refuted the wg-park hypothesis AT ALL g (interval
stabbing over 162k clean rows: coverage flat at ~80/74%, never the ~95% a
true park would give; the earlier rho~0.5 was a shared-centering artifact).
The peak is bias absorption: refined g_x = g_ext*(1+0.0481*2^-52), 64-bit
mantissa 0x906eba8214db6c6f (+-0.02*2^-52) — a bias correction. Best
composite C10r (j-pipeline RN53 parks + g_x): 67.65% (e=-25 35.3->64.2%).
Not decisive (closed op-graph ~90%+); b9heldout PRESERVED unraced.

Resting state: agentJ_resting_state.json — sharpened constraints (the
1.01/0.505-pub-ULP equidistributed component with grid ~ 2^Ez has ALL raced
sources refuted; per-binade coherent components largely explained except
e=-15/-20 fine phases) + three designed probes: (1) identify the 2^Ez-grid
source, (2) repair j-pipeline park phases at e=-15/-20 vs the banked per-row
residuals, (3) test parked-intermediate vs register-continuous chain floor.

## EXPM1 STAGING IDENTIFIED + LANDED (2026-07-18, agent R)

msvcr100 exports NO C99 expm1 (ctypes-confirmed; only msvcr120+ do) — Excel
builds its own from its primitives via **Kahan's cancellation-free correction
in DOUBLE arithmetic**:
    u = exp(t)                        (the x87 chain, RN53)
    if u == 1: return t
    if |t| < ~1: return (u - 1)*t / ln(u)    (ln = fyl2x RN53 == CR;
                                              numerator ONE product then the
                                              divide — orderings refuted)
    else: return u - 1
Python-model score 17,992/18,000 (fingerprint 99.88%); **PRODUCTION landing
with the real hardware chain: 17,996/18,000 = 99.978%** (9,997/10k EXPON +
7,999/8k a=1 rows — the real microcode closes half the idealized-model
residuals). Discriminators: all-extended collapses to ~CR (80.3%) — the
~0.5-ULP profile IS the double-rounding of the correction; pure-Kahan fails
x>=1; threshold ~1.0 (ln2 worse); DCDFLIB rexp / fdlibm / UCRT expm1 refuted.
The prior "extended F2XM1 -expm1 staging" claim was a =CR coincidence
(2/1971 fingerprint rows) — corrected.

LANDED (suite 1,606 green): excel_expm1_internal (excel_numeric);
EXPON.DIST cdf -> -expm1_internal(-lambda*x) (was the refuted 1-exp form),
pdf -> chain exp; WEIBULL.DIST cdf/pdf likewise (pow route still powf —
open lane); gratio a==1 P-side -> the identified expm1.

## Gamma-series staging: family EXHAUSTED, landed staging CONFIRMED (2026-07-18, agent Q)

- **The landed production staging IS the family winner**: forward Cephes-form
  gser (rr=a; c=1; ans=1; c*=y/rr; stop c/ans<=2^-53) + (r/a)*ans + exact
  (a-1)! normalizer + CHOP exp at the r-site. 38/45 at a=2 (vs RN/CR exp
  25/45 with ALL-NEGATIVE misses — the directed-rounding signature); chop
  dominates RN at EVERY b23A integer-a moderate-y slice.
- **wk-backward summation REFUTED** (18/45; worse everywhere) — the agent-I
  a=4 "reachability" preference was an artifact of the old staging
  assumption. The naive label-210 finite-sum P-view also refuted
  (catastrophic 1-Q at tiny y — but note tiny-y routes to path 20 anyway;
  production routing untouched).
- **Site-dependent publication RE-CONFIRMED on both sides** (the agent's
  "premise overturned" headline was a strawman of its brief): POISSON direct
  store = RN53 (chain RN 29,997/30,000 vs chop 49.9% — chop was never
  claimed there); series r-site = chop (validated above). The landed model
  is exactly this.
- **Exhaustion**: publication order, eps, stop rule, distributed-1/a, t1
  formation, x87 body modes, r-staging variants — ALL inert. The 7/45
  residual requires INCONSISTENT r+-1 (some rows near tiny F2XM1 fractions)
  = a chain-microdetail wall, same class as the 3/30k POISSON idealization
  rows. Method caveat banked: tiny-y/high-a rows are ln-amplification tests
  (+-30 ULP at y~1e-8), NOT series tests — series signal lives in low-a
  moderate-y.
- b26 batteries designed for the clean held-out gate (captured; scoring
  next): b26A integer-a moderate-y series gate, b26X cross-view, b26P
  POISSON re-confirm.

## b26 held-out gate (2026-07-18) — POISSON signed off; series staging held-out-confirmed with known ceiling

- **b26P POISSON: 4,000/4,000 through the production RN-chain path** — with
  b23's 30,000 that is 34,000 consecutive fresh rows, zero misses. The exp
  primitive + POISSON.DIST(0, lambda) are sign-off grade.
- b26A GAMMA.DIST (production path, integer-a moderate-y uniform grids):
  a=2 795/1600 (worst 4), a=3 544/1600 (worst 7), a=4 276/900 (worst 10).
  The staging holds held-out (the confirmed family winner); the ceiling is
  set by (i) the chain-microdetail +-1 class on r (the 7/45-type rows) and
  (ii) an error growing with a consistent with ln-amplification through
  a*L (worst 4->7->10). These are the two remaining named walls on the
  series path; both are primitive-microdetail class, below every staging
  axis (family exhausted).

## Lane 1 (2026-07-18) — distribution pow pinned; WEIBULL + EXPON bodies fully identified and signed off

Post-compaction sweep, lane 1 of the four-lane plan (land proven routes ->
clean residuals -> coefficient hunt). Work: `lane1_*.py` + `batch/answers-b27*`,
`b28*` in the G3-01 work dir; new tooling `check_pow_dist`, `check_weibull_pdf`,
`check_weibull_prod`, `check_expon_prod`, and the general **`x87_serve` op
server + `x87client.py`** (per-op hardware chain calls from Python — the tool
that cracked the pdf op-graph; use it for any future graph enumeration).

**Distribution pow staging (b24 re-race + b27 targeted capture):**
- Re-raced agentN's b24 verdicts with the REAL hardware chain (agentN had an
  idealized exp model): the exp-ln route is **33,145/33,145 across every b24
  block** (binom q^n 11,045 + p^n 4,400; weibull all 17 blocks) except one
  row (below). powf/chain-ext lose thousands; `powf` wins ZERO disagreements.
- b24 could NOT discriminate the product staging (plain `RN53(y·lnx)` vs
  POWER's double-rounded `RN53(RN64(y·lnx))`): every b24 exponent is
  low-entropy (integers <=720, dyadic fractions), so the RN64 step is EXACT
  and the stagings collapse. Designed-gap lesson banked: full-mantissa
  exponents are required to see the product rounding.
- **b27D targeted capture** (500k offline candidates -> 113 disagreement rows
  + 80 twins): **113/113 for the double-rounded product**, 0 plain, twins
  80/80. Distribution pow == `exp(RN53(RN64(y·ln x)))` — POWER's chain —
  but **WITHOUT the `0.5 -> sqrt` shortcut** (b24 s0p5: CR-sqrt 412/800 vs
  chain 800/800). The sqrt special case lives in the POWER *wrapper*, not
  the shared CRT pow. Landed as `excel_pow_chain` (excel_numeric);
  `excel_pow_positive` now delegates to it after the 0.5 check.

**WEIBULL.DIST identification (b27 pdf corpus 5,400 rows + b27b + b28):**
- cdf: `r = RN53(RN64(x/beta))` (x87 DR divide, b27b D2 2/2);
  `t = excel_pow_chain(r, alpha)`; publish `-expm1_internal(-t)`.
- pdf: **`alpha / pow(beta,alpha) * pow(x,alpha-1) * exp(-pow(x/beta,alpha))`
  evaluated LEFT-TO-RIGHT (division first!), every op double-rounded through
  a spilled double local** — the round-6 exhaustive tree×spill-mask race put
  `T3|SS` at 1,600/1,600 (Pb2+Pbf) where every other association order or
  spill pattern loses 300+ rows. All three pows are spilled-product chains
  (extended-argument delivery REFUTED per factor, round 5); the POWER-style
  reciprocal staging for alpha<1 REFUTED (direct signed-exponent chain).
- The identification path is a method exemplar: beta=1 blocks solved at 100%
  by the naive form, beta=2 (all beta-ops EXACT) still failed 157/400 —
  which forced the separate-powers hypothesis, since `pow(1,·)=exp(0)=1`
  makes the beta=1 world collapse to BOTH forms bit-identically. The C
  source line is readable off the bits.
- b27b D1 48/48: outer ops are x87-DR, plain SSE2 refuted directly.
- **b28 held-out (fresh 6,000 rows, production kernel): 5,999/6,000 =
  99.983%**, sole miss -2 ULP (chain-microdetail class, see clue ledger).
  LANDED in `weibull_dist_kernel`.

**EXPON.DIST (b28b + b28c):** body is the same legacy x87 per-op-DR class:
inner `lambda*x` 14/14 DR, pdf outer `lambda*e` 24/24 DR, twins 40/40.
Landed (`excel_x87_mul` at both sites). **b28c held-out (fresh 4,000 rows,
production): 4,000/4,000 = 100.000%.**

Big picture shift: the 2010 stats rewrite is NOT uniformly the plain-SSE2
world of GRATIO/BRATIO — the closed-form distribution bodies (WEIBULL,
EXPON) are legacy x87 compilation units with per-op double-rounded spills,
division-first C association, calling the same x87 transcendental CRT. Both
body classes coexist behind the same function surface. Wall implications
recorded in W109_WALL_CLUES_LEDGER.md.

## Lane 2 (2026-07-18) — POISSON pmf two-route structure; BINOM route localized to the internal-lgamma wall

Timeboxed per the cycle-back rule; no landings (no route reached sign-off).
Work: `lane2_*.py`, batteries b29 (BINOM 1,062 + NEGBINOM 1,800, banked).

**Corrections to prior verdicts (important):**
- The "POISSON direct-product route proven, ~21% unexplained at k=1" claim
  is WRONG and is hereby withdrawn: the k=0 window is ROUTE-BLIND
  (`0·lnλ − ln0! = 0` exactly, so `exp(−λ)` is common to product and
  log-composed routes). Direct product at k=1 scores 25.7% with ±10-ULP
  tails. Method lesson: a window that publishes a common subexpression
  proves the subexpression, never the route.

**POISSON pmf (k≥1) — two-route structure established:**
- k=2,3 at λ ≳ 14: **Loader's saddle-point dpois CONFIRMED bit-for-bit**
  (`exp(−stirlerr(k) − bd0(k,λ))/sqrt(2π k)`; dissect rows match Excel's
  ±50-ULP deviations from CR EXACTLY — route-confirmation of the strongest
  kind). stirlerr constants = CR doubles (mpmath-validated); bd0 direct
  branch, A-association `((x·L + np) − x)`, plain double.
- k=1 at large λ: NOT Loader (deltas −78 vs Excel's ±3). Excel ≡ the
  **extended-composed direct product** (`RN53(ext(powext(λ,1)·expext(−λ)))`,
  C4 class) exactly on all dissect rows. k=1 never matches Loader anywhere.
- Small-λ (all k): neither model as staged; mask families (per-intermediate
  spill × RZ × repeated-multiply pow, 128 masks) cap at 70/43/41%.
- Route-branch structure (why k=1 differs; where the small-λ staging
  changes) is the open question. All banked in the branch map
  (`lane2_poisson_branchmap.py` output).

**BINOM.DIST general k — route localized, not identified:**
- REFUTED at the exact-bit level: Loader dbinom (12%), direct
  `C·p^k·q^(n−k)` (all stagings ~8%), term recurrences from the proven k=0
  seed (~7%), log-composed with 9 argument stagings (8.8%), the 256-mask
  extended-graph family (~10%), published-GAMMALN-composed lnC (3%).
- **Implied-argument decode** (t = ln(pmf) at 200 digits, readable to
  ~0.02 ULP-of-argument): Excel's exp argument is log-composed-class,
  within ±2 ULP(arg) of `lnC + k·lnp + (n−k)·lnq`, residual bell ±1.5
  ULP already at k=1 (NOT k-accumulating), fractional part uniform
  (no double-lattice candidate inside ±0.6).
- Error calculus pins the source: published-GAMMALN-composed lnC is TOO
  WIDE (±6 observed for that candidate), plain-double compositions are TOO
  NARROW to explain ±2 — but three RN53-published large lgammas differenced
  give exactly the observed bell IF the lgamma is the sub-ULP **internal
  extended lgamma** (G3-02). **Leading hypothesis: BINOM pmf = exp-chain of
  an internal-lgamma-composed argument — the route is BLOCKED BY the
  internal-lgamma wall, and b29 + the implied-argument decode is a new
  MEASUREMENT WINDOW on that wall** (390+ decodable rows, each reading a
  3-lgamma combination to ~0.02 ULP).
- NEGBINOM: Loader dnbinom refuted (8.4%); presumably shares BINOM's route
  family (same lgamma composition with different integer arguments).

Next probes (designed, not run): (i) extreme-|t| b30 battery (p→0/1 edges,
bigger n) where the decode sharpens to <0.01 ULP(arg) and each row becomes a
linear constraint on the three internal-lgamma values; (ii) solve the
per-integer lgamma values from overdetermined row systems (same integers
recur across rows) — recovering internal lgamma AT INTEGER ARGUMENTS
bit-for-bit would crack G3-02's integer slice as a by-product.

**Lane-2 addendum (same day): the Loader control-flow smoking gun.** b29b
(BINOM.DIST(0, n, p<0.1), 400 fresh rows): Excel's k=0 switches formula
below p=0.1 EXACTLY as Loader's dbinom does — `exp(-bd0(n,nq) - np)`
matches 383/400 (the `n·ln q` form only 58, almost all where the two
coincide); 16 rows match neither (sub-staging of the bd0 series / compose).
The p<0.1 x==0 branch is a Loader-SPECIFIC fingerprint, so **BINOM
general-k IS dbinom_raw-shaped** — reconciling the implied-argument bell:
the Loader argument is algebraically `lnC + k·lnp + (n-k)·lnq` but computed
through stirlerr/bd0/lf ops whose roundings give exactly the observed ±2
ULP(arg) spread. The remaining unknown is the REALIZATION of stirlerr/bd0/
lf (my transcription: 12% exact; sub-stagings to enumerate: bd0 series loop
associations, lf = M_LN_2PI + log(x) + log1p(-x/n) with the log1p
realization, lc sum order, 0.5*lf staging, arg subtract order). The
internal-lgamma hypothesis is DEMOTED to secondary (the ±2 bell no longer
needs it) but the b29 decode-window instrument stands either way.

## Lane 3 (2026-07-18) — production re-score; two divergent OxFunc-side fast paths REMOVED

The lane-1/2 landings were verified regression-free (b22 baseline unchanged;
POISSON k=0 window 4,000/4,000). The re-score surfaced that BOTH pre-W109
integer-shape fast paths were silently overriding the identified kernels in
REAL production routing (all standing scores had been measured against the
substrate directly):

- **GAMMA.DIST cdf integer-shape fast path REMOVED** (`1 − e^{-x}·Σx^k/k!`):
  it scored 8.1% on b26 with ±4,400-ULP catastrophics (cancellation at tiny
  x: the b2-gser small-x rows showed 2^62-class deltas) vs 39.4% (worst −10)
  through the identified GRATIO path. Production ≡ gratio path verified
  bit-for-bit post-removal.
- **BETA.DIST cdf integer-shape fast path REMOVED** (binomial sum): b30
  capture (768 integer-shape rows): bratio 344/768 vs the shortcut 254/768,
  disagreement rows 177:87 for bratio; integer shapes behave at the SAME
  wall rate as fractional ⇒ **Excel has NO integer-shape beta special path**
  (resume item 8 first half MEASURED and closed).
- b30 Z-block (600 rows, A/B bounds): `z=(x−A)/(B−A)` staging broadly
  confirmed (wall-class rate 230/600, no structural misses) — bounds
  staging is not a separate wall; sub-ULP div/sub staging deferred.

**Post-lane-3 standing numbers** (production routing, bit-verified equal to
the identified substrate paths): CHIDIST 152/195; GAMMA.DIST modern corpus
293→**337/446**; b26 integer-a 331→**1,615/4,100** (worst −10); b22
**293/671** (integer rows now scored; BETA.DIST 136/288); b26 POISSON
4,000/4,000; WEIBULL b28 5,999/6,000; EXPON b28c 4,000/4,000.

Clue banked: GAMMA.DIST **pdf** (cumulative=FALSE) remains unmeasured and
production's log-composed pdf is now the prime suspect for the next
catastrophic class — by analogy with lane 2 (POISSON pmf = Loader/rcomp
class) and lane 1 (WEIBULL pdf = legacy direct), Excel's gamma pdf is
predicted to be an rcomp-class direct evaluation, NOT exp(log-pdf).

## Lane 5 (2026-07-18) — BINOM dbinom_raw sub-staging IDENTIFIED to the argument level; blocker consolidated onto the extended-entry-exp wall

Continuation of lane 2's bounded enumeration (`lane5_*.py`, b29 corpora).
The implied-argument decode (reads Excel's exp argument to ~0.06 ULP(arg)
at |t|>8) drove a four-round staging collapse:

1. **Round 1 (432 all-plain candidates): 56% → 87.5%** within ±0.7.
   Winners: bd0 direct association **B** (`x·L + (np−x)`), lc in R's exact
   source order (left-to-right), log1p realized as `ln((n−k)/n)`; series
   threshold 0.1 confirmed (0.125–0.15 statistically tied); np/nq product
   staging and quotient DR-ness indistinguishable.
2. **The fractional bell** (±0.25/±0.5 columns, non-integer — impossible
   for a double-vs-double comparison) forced the delivery question; the
   all-extended and per-return-extended (v3) models REFUTED (25%, 61%).
3. **The winning model (v2): Loader's literal C locals.** `lc` and `lf`
   are per-op DOUBLE locals (lc spill PROVEN — extended-lc collapses to
   19%); the final `lc − 0.5·lf` runs EXTENDED (RN64, unspilled) into the
   exp — the x87-side argument expression at the transcendental boundary.
   439/600 decodable rows at d≈0.00 exactly; 82.5% within the
   publication-noise criterion. This refines the campaign's central
   picture: SSE2 body, x87 transcendentals, and the LAST expression
   fragment before an exp call rides extended.
4. **End-to-end**: extended entry is the only surviving publication class
   (34.2% overall; call-boundary-spill variants collapse to 7% at t≥8) —
   but on correct-argument rows the composed extended-entry chain
   (`exp_chain_from_ext`) agrees with Excel's published bits only ~45%.
   **The blocker is the extended-entry fFEXP realization — THE SAME
   unknown as the erf 190-path C10r plateau (wall 3).** k=0 control: the
   p<0.1 branch closes at 383/400 (95.8%) where the argument is a plain
   double — the contrast isolates the wall to the extended-argument entry.

**Major new instrument for wall 3:** the ~500 correct-argument b29 rows
are (extended-argument, published-value) PAIRS — a direct oracle for the
extended-entry exp that the erf lane never had (erf's arguments were never
exactly recoverable). Attack the chain realization there, not on erf.

No landing (never accept a divergence: end-to-end is chain-blocked), but
the BINOM route + argument staging is now identified end-to-end modulo one
shared primitive; NEGBINOM presumably identical (+ its `size/(size+x)`
prefactor). Files: lane5_binom_enum/diag/threshold/attrib/extmodel/mixed/
final_model/v3/v2_polish/lclf_mask/e2e_final/pubvariants/k0_confirm.py;
new server op `cexpext2 hi lo` (extended-argument chain entry).

## Lane 6 (2026-07-18) — the extended-entry chain is EXONERATED; the wall moves to sub-double argument content

Attack on the b29 oracle pairs (`lane6_*.py`; new server ops `lnext` —
hardware fyl2x extended result as hi+lo — and the `cexpext2` entry).

**Headline: the composed extended-entry fFEXP chain IS Excel's exp for
extended arguments.** The j-interval scan (chain output vs published bits
as the argument steps in ulp64 units around the model value) finds a
consistent argument for **76% of rows within ±70 ulp64**; the 24%
no-window rows are the known ±1-term class (arg off by ~2048 ulp64 —
outside the scan, not chain-refuting). The chain realization question that
defined wall 3 is ANSWERED at this site: given the right 64-bit argument,
`exp_chain_from_ext` reproduces Excel bit-for-bit. **Wall 3's erf C10r
plateau should be re-read as ARGUMENT-side (sub-double delivery details),
not chain-side.**

What remains: the argument's low ~11 bits (below the implied-decode floor
of ~0.06 ulp53). Since lc's RN53 spill is proven, the sub-double content
comes through `0.5·lf` — but the narrow-interval solver (rows pinned to
±8 ulp64) rejects every single-source hypothesis tried: lf-as-double
(H0: 35/137), lf ext-sum-of-ln53s (H1: 41/137), lf with hardware-extended
lns (H2: 33/137), 77 rows OTHER. Unexplained narrow rows CLUSTER AT
EXTREME p (0.9999+, 1e-5) with deviations reaching the ±70 scan boundary
(~0.05 ulp53) — a second, p-extremity-correlated source. End-to-end
plateau this round: 36.4% (lf-extended variant best; last-bit combos
t×c×f all within 34.2–36.4%).

Next probes (designed): (i) run the narrow-interval solver with the scan
widened to ±300 ulp64 and the ±1-term rows' terms nudged (joint solve of
term-ULP corrections + sub-double content); (ii) regress narrow-row
deltas against per-row candidate tails (0.5·lf variants, b-term extended
returns, np/nq product tails) — the delta is a LINEAR read of whichever
tail is real; (iii) transfer to erf: run the same j-scan on the b9heldout
erf rows using C10r's argument model — if intervals exist there too, the
plateau is argument-side and the two walls merge completely.

## Lane 6b (2026-07-18) — erf j-scan merge test: CONFIRMED, walls 3 and the BINOM blocker are one

Ran the j-interval scan on the erf 190-path development corpus (1,508
distinct z<0.5 rows from b9train/erfp/erfm/b7/b8/b10/b11 — **b9heldout
untouched**), sliding the chain argument `zl = a·ln_ext(x)` in ulp64 steps
(±240 ≈ ±3 pub-ULP) through the faithful C10r pipeline (series/j RN53,
two-step RN53 inner, pinned 64-bit g_x mantissa 0x906eba8214db6c6f,
w extended into `RN53(ext(w · ext(g_x·inner)))`). New racer mode:
`check_erf190 <dir> jscan`.

**Result — the BINOM signature, almost number-for-number:**
- windowed **1,154/1,508 = 76.5%** (BINOM: 76%) — a consistent argument
  EXISTS; the composed extended-entry chain + C10r publication reproduces
  Excel bit-for-bit given the right 80-bit argument.
- j=0 exact 52.4% — the model argument already lands in its window half
  the time.
- centers: median 0, dominant 0-bin (380 rows), symmetric spread to ±240
  ulp64 — the same sub-double argument scatter as BINOM's.
- no-window **23.5%** (BINOM: 24%) — rows unreachable by ANY argument
  shift: the DOWNSTREAM visible-level class (j-pipeline park phases at
  e=−15/−20, the g_x last-bit business) — erf's analogue of BINOM's
  ±1-term rows.

**The two walls are formally ONE:** at every identified extended-entry exp
site, (i) the chain itself is our composed hardware chain — exonerated;
(ii) a per-site visible-level term class (~24%) needs its own repair; and
(iii) the remaining unknown is the argument's SUB-DOUBLE content — how the
32-bit codegen composes the last expression fragment (`a·ln_ext(x)` here,
`lc − 0.5·lf` in BINOM) at 64-bit before the chain consumes it. One
unknown, two corpora now, with the narrow-interval solver as the shared
instrument. Closing it closes: erf 190-path (and its CHIDIST/GAMMA.DIST
inheritance), BINOM, NEGBINOM, and likely the POISSON small-λ side.

## Lane 6c (2026-07-18) — joint sub-double solve: both flagship hypotheses refuted; epistemic sharpening of the unified wall

Joint solve across both corpora (`lane6c_*.py`, `check_erf190 hyp` mode).

**Refuted this round (all end-to-end, both sites where applicable):**
- erf: x²-spill-into-ln variants (V0..V3 mixed spill/extended for ln vs
  series) — all 51.9–52.4%, indistinguishable. The x-delivery sub-double
  difference almost never moves the published bits.
- BINOM: M_LN_2PI-as-tbyte (extended constant) — WORSE (32.5% vs 36.4%)
  with a +1 bias; hardware-extended lns in lf — worse; every lf
  composition variant remains in 32–36%.
- The chain-error-map hypothesis: needed correction c vs the F2XM1
  reduction fraction f = t − rint(t) is FLAT across all f-bins (weak
  uptick only at the |f|≈0.5 reduction boundary) — the ±1 scatter is not
  a simple deterministic function of f. CAVEAT: run on ALL rows; the
  term-class rows (~24-35%) dilute — the designed re-run filters to the
  argument-certain subset (d≈0 rows) and compares the c(f) map ACROSS
  BOTH corpora.

**Epistemic sharpening (important, banked):**
1. With lc/lf proven doubles and the final subtract exact-at-64-bit, the
   BINOM argument family is CLOSED — the argument is fully determined.
   Since no composition variant reaches the windowed ceiling, the ±1
   residual must live in the chain/publication realization for extended
   arguments — BUT:
2. The windowed-76% result is WEAKER than lane 6 claimed: any monotone
   chain with the same output granularity windows almost every reachable
   published value. Window existence ≠ chain exoneration. The real
   discriminators are (i) the no-window class (published values needing
   args > 240 ulp64 away — the visible-level term classes, confirmed) and
   (ii) structure in the needed-correction map on argument-certain rows.
3. Current best factual summary of the unified wall: argument families
   closed at both sites; composed-chain publication ±1-scatter on ~half
   the argument-certain rows; scatter not explained by f-fraction,
   lf/x composition tails, or constant precision.

**Designed next probes:** (i) c(f)-map on argument-certain subsets of BOTH
corpora simultaneously (same map ⇒ chain-side, different ⇒ residual
argument leak); (ii) exact-pair search: rows across corpora whose model
extended args agree to <1 ulp64 — their published values must then agree
via ANY deterministic chain (a chain-side litmus with no model
assumptions); (iii) widen the BINOM narrow-interval solve to ±300 with
joint term-ULP nudges (the ±1-term rows currently pollute every map).

## Lane 6d (2026-07-18) — exact-constraint reframing; pair search retired by arithmetic; the crossing-sweep is the right instrument

Methodological reset (user directive: deterministic noise-free inverse
problem — every bit counts; stop steering by match rates):

**Information-budget statement of the wall.** Each row is one exact
equation `published = RN53(CHAIN(arg))`. The implied-argument decode floor
(±0.06 ulp53) EQUALS the publication granularity in argument space
(~2^-52.5) — a single (model-arg, published) read therefore carries no
independent information about which side of the output boundary the true
internal value sits. The ±1 "scatter" lives entirely below the
single-read resolution; percentage scores there measure model phase, not
truth. Progress requires multi-read constraints.

**Pair search (run, null, retired):** zero within-BINOM pairs at every
threshold up to 64 ulp64 — b29's 1,062 args are ~10^17 ulp64 apart.
Collisions cannot be designed either: the p-dial's finest step moves the
argument ~256 ulp64 (2^8 too coarse). Exact-argument pairs are
structurally unreachable at this site. (Cross-corpus pairs are further
model-polluted by erf's post-multiplier.)

**The correct instrument — boundary-crossing sweeps (b33 design):**
sweep p in 1-ulp steps for fixed (k, n): the argument walks in ~256-ulp64
steps, the published value steps a staircase, and each TRANSITION pins
`CHAIN(arg)` against a known rounding boundary to one p-step — an exact
inequality per crossing, ~8x tighter than a single read, hundreds of
crossings per sweep. Compare observed crossing positions with our
composed chain's predictions: agreements/disagreements map the chain (or
residual-argument) deviation bit by bit. This is the erf tooth-law
bisection method (oracle-batched boundary localization to ~2^-66) applied
with a KNOWN argument model — the first time both sides of the equation
are available. Design: 4 anchors (k,n) ∈ {(1,12),(2,24),(3,48),(5,64)},
p-windows chosen so |arg| spans 10–600 (the ulp64/output-granularity
ratio varies 4..256 across that range — the low-|arg| end reads the
argument, the high-|arg| end reads the chain); predict crossings offline
with cexpext2, capture ±8-ulp p-brackets around ~200 predicted crossings
per anchor (~7k probes), score crossing-position deltas exactly.

## Lane 7 (2026-07-18) — b33 crossing sweep RUN: the wall resolves into per-window integer-ULP term corrections

b33 captured (18,000 probes: 4 anchors × 3 windows × 1,500 consecutive
p-ULPs; `lane7_b33*.py`). Instrument notes: the p-walk is faster than
designed (3–1,066 output-ulps/step; slow-walk windows need near-mode p),
so crossing-matching only read the single-ulp staircase segments — but
those alone yielded **1,093/1,258 matched crossings at delta EXACTLY 0**
(A2 w1/w2: 853/853 at zero). The full-staircase shift analysis + per-window
term attribution then produced the decisive picture:

**Every window carries a CONSTANT argument offset of ±(1–4)·2⁻⁵³, and a
single ULP-level nudge of ONE term makes the window land bit-exactly:**
- A1 (k=1,n=12): w1 `M+1` → **60/60**; w2 `M+1` → 55/60 (same shift both
  windows ⇒ lf-side constant realization for this anchor; w0 = the
  near-mode window, less determined).
- A2 (k=2,n=24): w1 `b1+1` → **58/60**; w2 `lp−3` → 46/60; w0 mixed.
- A3 (k=3,n=48): w0 needs +1·2⁻⁵³, w2 needs +2·2⁻⁵³ (p-VARYING ⇒
  bd0-side realization); w1 unresolved in the ±6 nudge range.
- A4 (k=5,n=64): w1 needs −4·2⁻⁵³ (42/60), w2 −2·2⁻⁵³ (34/60) —
  p-varying ⇒ bd0-side.

Notes: the nudge attribution identifies the SHIFT QUANTUM, not the term
(M/lk/lp shifts are near-degenerate at 2⁻⁵³ scale); stirlerr nudges are
inert (their ulps ~2⁻⁶² are below the resolution — stirlerr realizations
are NOT the wall). The chain is now exonerated with positive evidence:
whole windows reproduce Excel's staircase exactly under one term
correction — the deviation is NOT in the exp.

**The endgame program (bounded, linear):** capture MANY short windows per
anchor spanning p; each window yields one exact equation
"needed shift = Σ (term corrections)"; same-anchor windows share the
lf-side unknowns while bd0-side unknowns vary with (branch, magnitude
class) — an integer-ULP linear system over a handful of unknowns per
class. Solve, then identify WHICH published realization (bd0 variant,
lf composition, constant provenance) produces exactly those values.
The b33 answers + scripts are the template; ~10 more windows per anchor
(15k probes) should overdetermine every class.

## Lane 8 round 1 (2026-07-18, agent-T) — b34 interval solve: log1p RECOVERED; exact instrument built

b34 captured (24,000 probes: 6 anchors × 10 windows × 400 p-ULPs; two k=1
anchors isolate the M+lp side). Agent-T deliverables: agentT_results.md +
agentT_{intervals,deltaw,system,delivery,classes}.json.

- **Exact interval instrument:** all 24,000 rows converted to hardware-
  chain preimage intervals of the published double (~ulp64 resolution,
  0 clamps) — candidate realizations now test OFFLINE with zero chain
  calls. Verified faithful against the end-to-end path.
- **IDENTIFIED: `lp = log1p(−k/n)`** — R's literal dbinom_raw source line;
  the pinned `ln((n−k)/n)` was wrong. With M_LN_2PI at +1 ulp, B2's clean
  windows go 0 → 363/400. bd0-direct does NOT use log1p (keeps plain
  log(x/np) — the log1p swap there scores worse).
- Structure proven from the intervals: delivery EXTENDED (extreme-p
  windows admit 0/400 representable doubles under RN53 delivery);
  windows class-homogeneous (no in-window branch/binade splits); lc
  re-confirmed a spilled double; stirlerr re-confirmed inert (2⁻⁵⁸).
- Clean-window offsets are OPERAND-CONTINUOUS fractions of ulp53(b1)
  (−0.92, +0.99, …) — the bd0-direct product consumes something extended
  (predicts the L-unspilled variant).
- Round-2 (running): hardware FYL2XP1 log1p (new server ops lp1/lp1ext)
  — the x87 instruction BUILT for log1p — and the 16-mask bd0dir
  op-graph family, raced offline against the banked intervals.

## Lane 8 round 2 (2026-07-18, agent-T) — term-correction model REFUTED by infeasibility proof; deviation relocated to chain entry

- **Hardware FYL2XP1 ≡ CR-log1p at RN53 on every argument in play** (all 6
  b34 anchors + all 59 b29 (k,n) pairs bit-identical) — the round-1 log1p
  identification IS the hardware result; b29's residual is not a
  log1p-rounding artifact. Global best realization: lp1 — b34 7,749/24,000,
  b29 366/1,062. lp1ext refuted globally (helps only B5-w06..08); the
  M+1ulp coupling is B2-anchor-local (a surrogate for a −2·2⁻⁵³ constant,
  NOT an M identification).
- **bd0dir op-graph family EXHAUSTED**: all 96 (16 masks × 3 lp × 2 M)
  candidates raced offline against the 24k intervals; every nonzero mask
  equal-or-worse; B4/B6 direct/direct clean windows score 0/400 under ALL
  candidates.
- **THE TERM-CORRECTION SYSTEM IS INFEASIBLE — exact proof**: same-anchor
  same-class clean windows pin δ_w to mutually incompatible sub-ulp
  constants (B6-w06/07/08 = −1.8591/−2.0466/−2.0312·2⁻⁵³, spread
  0.2·2⁻⁵³ ≪ ulp53(b1) = 16–128·2⁻⁵³). No double-valued term correction
  can produce that. All stirlerr realizations excluded exactly (≤0.03·2⁻⁵³
  bounds, 60× below the bodies).
- Residual shape (per-window constants ±2·2⁻⁵³, sub-ulp grid,
  non-monotone 0.1–0.2·2⁻⁵³ drift) points at the CHAIN-ENTRY side —
  re-opening lane 6c's caveat with clean per-window constant reads.
- **Round 3 (running): the INLINED-INTRINSIC hypothesis** — the chain
  arithmetic under the application-default CW PC=53 (F2XM1 unaffected by
  PC; the legacy CRT sets 0x133F but an inlined chain runs under the app
  CW). New server op cexpext2p53; smoke test: exp(10) differs from the
  PC64 chain by 2 output-ULPs. Plus the free δ_w-vs-reduction-state map.

## Lane 8 round 3 (2026-07-18, agent-T) — PC53 refuted; the wall decomposes into TWO exact layers

- **PC53 inlined-chain hypothesis REFUTED end-to-end** (b34 17–19%, b29
  collapses to ~10%; the B4/B6 discriminator windows stay dead). The true
  chain is the full-PC64 CRT class.
- **Reduction-state map banked** (agentT_redmap.json, all 60 windows):
  the per-window body constants follow NO law in the reduction fraction f
  or parity — any future chain hypothesis tests against this table free.
- **POSITIVE: exact two-layer decomposition** — δ_w = body_w + m_w·ulp53(arg),
  m ∈ {−1,0,+1}: the wild windows are the anchor body ± exactly one
  ulp53(arg) (B1-w08 −8·2⁻⁵³ at |arg|∈[8,16); B3-w09 +64·2⁻⁵³ at
  [64,128); B4-w06 −32·2⁻⁵³ at [32,64); residuals ≤0.06·2⁻⁵³), and the
  bimodal windows flip m row-by-row. Since lc and arg share a binade,
  **layer 1 = ±1 ulp of the final lc subtraction** — lanes 6/7's entire
  "±1-term / no-window" class, now exactly identified. Layer 2 = the
  smooth ±2·2⁻⁵³ body with 0.1–0.2·2⁻⁵³ drift, outside every raced
  realization.
- Round 4 (running): mixed-PC chains (p53r/p53s), tbyte-park control
  (cexpext2mem), reduction-subtract chop (cexpext2rz) — racing against
  the intervals with the body isolated (layer-1 subtracted).

## Lane 8 round 4 (2026-07-18, agent-T) — all chain variants refuted with structure; the magnitude theorem; b35 approved

- mem tbyte-park control ≡ baseline BIT-EXACT (harness transparency
  proven). cexpext2rz ≡ baseline everywhere: **the reduction subtract is
  always Sterbenz-exact at 64 bits — its RC is unobservable; chop
  hypotheses at that site are vacuous** (durable fact).
- p53r/p53s refuted; p53r additionally shows re-bracketing depth
  collapse: a PC53 reduction jitters per-row, and the observed depth-400
  per-window constancy **structurally excludes any jittery reduction —
  the true chain's reduction is exact**.
- Bonus refutations (offline vs the intervals): lf as single
  ln(2π·k·(n−k)/n) — predicted bodies (0,+1,0,+2,0,0) vs measured
  (+2,−2.2,+0.5,+2.5,−0.55,−2); fdlibm-class polynomial exp at PC64 on
  the extended arg TIES the F2XM1 chain (34.46% b29 — the chain algorithm
  is not what the body discriminates); pure-double fdlibm 14% —
  extended-content consumption reconfirmed CHAIN-INDEPENDENTLY.
- **Magnitude theorem (banked)**: the body is ±0.2–2.7 output-ULPs ≈
  400–5,500 ulp64 — no extended-op micro-detail can produce it. Remaining
  possibilities: algorithm-level approximation error (tied), an unmodeled
  double-rounding between core and publication, or unraced argument
  staging. The wall needs DATA: **b35 approved** — 6 anchors × 3 matched
  model-argument targets (−20/−50/−100) × 400 p-ULPs; decision rule:
  matched-arg bodies equal across anchors ⇒ chain-side deterministic map
  (then one dense sweep reads δ(arg) completely); differ ⇒ argument-side,
  k=1 anchors isolate lf. Either branch converts the wall into a
  determined read.

## Lane 8 round 5 (2026-07-18, agent-T + b35) — FORK DECIDED ARGUMENT-SIDE; lf IDENTIFIED: log1p ported as TWO SEPARATE LNS; the plateau breaks

- **Fork verdict: ARGUMENT-SIDE.** At every matched-argument target the
  bodies DIFFER across anchors by up to 4·2⁻⁵³ (chain exonerated with
  positive cross-anchor evidence — same argument, different bodies, per
  anchor family).
- **IDENTIFICATION: `lf = (M_LN_2PI + ln k) + (ln(n−k) − ln n)`** — R's
  `log1p(−x/n)` realized as a DIFFERENCE OF TWO SEPARATE HARDWARE LNS.
  msvcr100 exports no C99 log1p (exactly as it exports no expm1 — the
  same porting hole, patched the plain way this time). Betrayed by the
  demanded per-anchor δlf parity vector (0,0,0,−1,0,+1) = ∓1 ulp of lf,
  which exactly one raced staging produces. bd0's quotient-ln stays a
  single ln (2-ln bd0 raced: worse everywhere); left-to-right grouping
  confirmed; stirlerr tiers re-refuted numerically.
- **Verified end-to-end (real chain):** b29 34.46% → **45.10%** (the
  lane-5/6/7 plateau broken, +11 points); b34 32.29 → 48.06%; b35
  45.43 → 68.58%. The dead windows land: B6-w05..09 = 400/355/382/386/400
  from 0/400.
- **Remaining (exact residuals banked in agentT_results.md):** B6
  essentially closed (≤0.14·2⁻⁵³); residual concentrates on small-n/small-
  operand anchors (B1 +1.98, B2 −1.1..−1.7 ·2⁻⁵³ — bd0-direct staging at
  small np), the series-branch staging, and the layer-1 ±1·ulp53(lc)
  class. Designed next probes named. Production landing still gated on
  those (never accept a divergence), but the argument model now has TWO
  recovered source lines (log1p form; its 2-ln realization) and one
  named porting hole.

## Lane 8 round 6 (2026-07-18, agent-T) — layer-1 IDENTIFIED: the lc grouping; bd0/series families exhausted

- **Layer-1 = the lc GROUPING: `lc = ((s1−s2)−(s3+b1))−b2` (O3).** On the
  clean domain it predicts 403/475 measured ±1-ulp53(lc) flips with ZERO
  false positives (97.8% all-row agreement); all 11 alternative groupings
  predict nothing or break hundreds of zero-rows; adjacent groupings lose
  6–21 end-to-end points. Third recovered source line of the lane (after
  the log1p form and its 2-ln realization): the C expression associates
  (stirlerr(n−k) + bd0(k,np)) before subtracting.
- **Cumulative model end-to-end: b29 49.81%** (34.46 at lane-6 close →
  45.10 after 2lnA → 49.81 with O3), b34 52.17%, b35 75.51% — three-corpus
  consistent.
- bd0-direct staging family EXHAUSTED at small operands (9 more candidates
  incl. the split-log analogue — the log1p lesson does NOT extend to bd0;
  recip-mul, distributed, deep-split, ext-ST0-return all refuted with
  margins). Series staging INERT (all variants tie within 3 rows).
- New instrument: absolute-interval bank (agentT_intervals_abs.json,
  31,200 rows) — all future racing zero-chain-call.
- Remaining, exactly characterized: (a) 72/475 flips from a second rarer
  source (DR-quotient rows the first suspect); (b) the small-operand
  smooth bodies (B1/B2/B3/B5, ±0.2–2·2⁻⁵³, arg-varying) — outside every
  raced staging family; next battery designs live with the banked
  intervals.
