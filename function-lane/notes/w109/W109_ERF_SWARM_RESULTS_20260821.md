# ERF/GAUSS/NORMSDIST theory swarm — results and corrections

Date: 2026-08-21
Lane: W109 inverse-problem / calc-graph search
Parent: `W109_ERF_GAUSS_NORMSDIST_THEORY_HANDOFF_20260821.md` (the shared prior
this swarm attacked). This document records what the swarm established, what it
refuted — including several sections of the handoff itself — and the capture
queue it produced. It is not a closure claim.

Method: eight proposal agents (A–H per handoff §15), each followed by an
independent adversarial verifier that re-ran the load-bearing computations with
fresh code. All work was offline: no Excel/COM was launched, no heldout was
opened (`answers-b9heldout.json` and both GAUSS heldouts untouched), no frozen
corpus was resampled, no Microsoft binary inspected. Verifier verdicts:
A/B/C/D/F/G CONFIRMED, E PLAUSIBLE (two quantitative corrections noted below),
H FLAWED **on its discriminator only** (science confirmed; capture legs must be
re-scoped before execution).

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial` (G-F3 / G-A400 dispatch integrated;
  ERFC body still scaffolding)
- `open_lanes`: ERF/ERFC.PRECISE body; GAUSS/NORMSDIST residual inherited from
  that body; tiny-route comb/grain after the G-A400 dataflow; hygiene lane (§8)

The G-F3 NORMSDIST wrapper and derived GAUSS (including stored-z tiny-direct)
are now in the production kernels — see §10 and
[`W109_NORMSDIST_GF3_WRAPPER_20260821.md`](W109_NORMSDIST_GF3_WRAPPER_20260821.md).
That is a wrapper landing on the still-open ERFC body, analogous to
`CHIDIST(df=1)` through `ERFC.PRECISE(SQRT(x/2))`. Capture scripts remain
designs; oracle execution stays with the serialized root lane. Heldouts stay
sealed.

---

## 1. Headline results

| Agent | Verdict | Result |
|---|---|---|
| A | CONFIRMED | The 480 tied tiny-direct graphs are exactly two arithmetics, G-A80 (x87 w-recovery, w stored to binary64 before the g-multiply) vs G-A400 (reuse of stored z), 1 ULP apart on all 14 separator inputs. Full 28-prediction answer key produced and double-validated (hardware x87 + independent exact-integer model). Per-op-binary64 `gam1(½)` bit-pinned: **h = `0x3fc06eba8214db6b`** (pure-SSE per-op gives the same bits). The common 336-row residual is a deterministic, odd, positive-biased sawtooth in z-mantissa (period ≈6 input-ULPs at 1e-15, absolute-locked across binade crossings, amplitude ~0.7 ULP undiminished 900 binades deep) that **no** arrangement of 15 raced store/constant axes reproduces. |
| B | CONFIRMED | **The handoff §4.4 tooth law is grid/protocol aliasing.** Every headline constant is alias arithmetic: ramp +0.145 and drop −0.855 are `frac(g·2^45) = 876/1024` (the low bits of the model constant g itself); the 3× collapse at m = 2/g is the ans-binade ULP doubling (`876/2048`); the "m=1.5 half-quantum slip" is an ordinary 7-gap of a 6.098-step rotation; the bisected p(e=−30) = 2.996·2⁻³⁶ is bracket-geometry-bounded ([2.993, 2.997]·2⁻³⁶) and carries no generator information. The 10×-refinement rule executed: the slow sawtooth is flat-absent on the 128×-finer b16 grid (same oracle, bit-identical shared rows 128/128). What survives: the residual is a **mantissa-only, binade-invariant deterministic comb** (eps(e=−30) ≡ eps(e=−40) row-by-row, corr +0.9999) with a two-regime variance split that **proves the inner complement cluster is RN53-staged** (pure-Ext80 inner refuted; j visible only for x ≥ 9·2⁻⁵⁵, matching the clean {−30,−40} vs elevated {−25,−20,−15} split exactly). Comb frequency determined only mod 2⁵² by the all-dyadic grids (~100 candidates/family — constraints, not an identification). |
| C | CONFIRMED | **T1c is dead on the 190-path.** The b25 read (independent replication of the 2026-07-18 agentJ read — the handoff §15 premise "never read" was stale): the residual is **exp-result-relative** — width 0.896 dbl-ULP of w, frame-constant at CV 1.1% across ans-mantissa 1.37→1.99→1.00, vs CV 17.9% for the ln-absolute frame; the smooth bias component also halves across the ans-binade crossing (0.934→0.473 etc.). Both residual components live on the **w double grid** (2^Ez), not the ln(x) grid. Chop re-refuted at full scale (15,453 down / 43,238 up flips). A plain full RN53 w-park (width exactly 1.0) is ~10% too wide against a 2–4%-calibrated estimator. |
| D | CONFIRMED | The assigned stored-z² lead is **refuted** (binade-bottom separator has 118/778 false positives; z² essentially exact at the five k-rows; 0/6 Ext80→RN53 double-rounding divergences). The six decoded-Q landmarks are instead the ordinary **P-side −1-ULP tooth** seen through a quarter-ulp(Q) phase/parity visibility window that is open only in the 1/8 binade (H-D1): all six become bit-exact with internal p = plateau−1 (admissible common window (−1.032, −0.990) ulp(p) — the integer −1, not a fit). Direct corroboration already frozen: `ERF.PRECISE(1/8) = 0x3fc1f5e1a35c3b89` = plateau−1 in four banks. Exhaustive 2,592-config mixed ext64/native53 store-site race: ceiling 778/784, zero configs hit the six. Best generator-class lead (not landed): per-op-53 stored `z·g` cluster hits 5/6 with the right period class (8.15k) but wrong duty/phase. |
| E | PLAUSIBLE | Tail (z ≥ 0.5) staging confirmed per-op binary64 with **unsplit** `exp(−RN53(z·z))` and PHI-class DBL_MIN flush (Cody XBIG re-refuted; last finite at RN(26.543)+1ulp publishes in the bottom normal binade, ~209 bottom-binade ULP from CR truth yet 0 ULP from the unsplit-w model). Best **named** graph: Cody-1969/SPECFUN rationals with unsplit exp — 3,218/3,557 (beats plateau 3,181), direct 113/355 vs libm 84/355 max 212. **Killed on tail rows**: NSWC/CDFLIB erfc1 tail (2,357/3,557 — the same-source-tree erfc theory fails at the coefficients), gratio a=½ CF routing (contradicts Q-primary direction; shape-uncorrelated), Cephes, SLATEC, Chiarella-Reichel, extended-product delivery, every stored-log-scale intermediate. Verifier corrections: the idealized-F family ceiling on direct rows is **146/355** (not 114 — Cody is NOT at the ceiling; ~30–55 rows of named-F headroom remain; NSWC double-precision DERFC1 (TR 92/425) is the named next candidate); the +4.33 residual extreme does not exist (max +4.17). Residual after unsplit-w: stdev 1.82 (2⁻⁵³ rel), extremes −7.09 (z=1.875) / +4.17, decorrelates at 1-ULP z spacing. |
| F | CONFIRMED | **NORMSDIST is NOT 0.5+GAUSS.** G-F3: `NS(x<0) = RN53(0.5·Q(z))`, `NS(x≥0) = RN53(1 − 0.5·Q(z))` with the stored-multiply z — the sign-split **without** the trailing −0.5. H-F1 (0.5+GAUSS) and H-F2 (P-side) each refuted by **14,122 model-independent structural witnesses** in `answers-b24-normref.json` (rows off the forced 2⁻⁵⁴ grid) plus 5,280 nonzero tail rows where both rivals force a hard zero. GAUSS is derived: **GAUSS = NORMSDIST's graph with a trailing −0.5** — which explains every sparse 19/22-style hit (Sterbenz band), the non-odd GAUSS bank pairs at ±2⁻⁴⁴/±2⁻⁴⁹, and re-derives GAUSS(2⁻⁴⁹) = `0x3cc8000000000000` as ties-to-even RNE(13/2). Cross-surface pins: NS(−1) and NS(−0.5) are bit-exact halves of `CHIDIST(1,1)`/`CHIDIST(0.25,1)` at shared z. Novel falsifier: NS(−37.52) = +0 while same-sheet ERFC.PRECISE(z) stays finite. **Corollary: b24-normref is a 16,495-row implied-Q bank (Q = 2·NS exactly) at fresh z ∈ [0.035, 25.5] with zero overlap with any ERF/ERFC bank — new tail oracle for agents D/E.** |
| G | CONFIRMED | Complement-direction law reproduced offline bit-for-bit (700/700, zero exceptions; compensated 649/700 re-killed; boundary flip bracketed to (0x3fde700000000000, 0x3fe0000000000001], consistent with exactly 0.5). **No seam at 1.375** (smooth resolution decay; CR-residual bucket scan flat across it) — 1.375 was a capture-design label. Cross-channel Q consistency **330/330** (ERFC direct / CHIDIST(2z²,1) / GAUSS-decode) — one-body thesis intact. New: the complement subtract's store site (SSE-double vs x87 RN64→RN53 spill) is **unobservable on every existing bank** (0/699 splitters; 1−P exactly representable in Ext80 for P ≥ 2⁻¹²); 79 breaker inputs mined from banked P < 2⁻¹¹ rows where the two stagings publish different ERFC bits (`agentG_subtract_breakers.json`). |
| H | FLAWED (discriminator) / science CONFIRMED | **The inferred Ext80 gam1(½) mantissa `0x906eba8214db6c6f` is a phantom** — a corpus-weighted phase average of the residual. Exact-rational interval mining over the collapsed tiny model (j ≤ 2⁻¹⁰²·¹, so all association/spill axes reduce to `RN53(RN64(z·g)/2)`): global intersection EMPTY; constant-g ceiling 2,836/3,158 (the §5 "±4096 scan flat" row was staging-specific — annotate it); g_x itself covers only 967/3,158; three region pins on one surface are pairwise disjoint (dyadic band nonempty at −(1778..331) ulp64 from g_x; e=−51 window and e=−53 ladder each EMPTY); b18's ERF e≤−40 band averages to g_x+6 while the GAUSS bank averages to g_x−337. **T1a's wrong-gam1 story is dead on the tiny route**; w-recovery choice also dead there (chain error two orders too small). Hard replacement constraints: the dyadic transport law GAUSS(2^k) = 2^k·PHI(0)-mantissa holds on **971/971** positive direct dyadics k = −50..−1020. Discriminator flaw: its "fresh" dyadic rows are all already in-bank (already answered `…51` — replication, not discrimination); the valid fresh legs are the 12-row window `0x3cd0000000000100..10b`, the deep full-mantissa probes, and the ERF.PRECISE same-z cross-read. Re-scope `Run-GEffTightening.ps1` before any capture. |

---

## 2. Theory scoreboard after the swarm

- **T1a (faithful 190 + unknown spill/association):** dead in its "wrong gam1"
  form (H: no constant exists; phantom mantissa) and in its "spill schedule"
  form on the tiny route (A: 15 axes raced, nothing reproduces the sawtooth;
  H: axes provably collapse under the j-bound). What survives of T1a is its
  skeleton: branch-190 dataflow with **more RN53 stores than assumed** —
  B proved the inner complement cluster is RN53-staged; gam1 is per-op
  binary64 (h = `0x3fc06eba8214db6b`); D's best generator lead is a per-op-53
  stored-product cluster.
- **T1b (fused/rearranged j-cluster):** unresolved but constrained — B's P2/P3
  capture predicts different clean/elevated break rows for
  `0.5+RN53(0.5−j)` (variant A) vs fused `RN53(1−j)` (variant B); the tiny
  route is j-free, so T1b cannot generate the tiny residual.
- **T1c (double-precision LN residual, tight EXP):** **killed** on the
  190-path (C), independently corroborated by B (any zl-lattice mechanism
  destroys the e=−30/−40 binade invariance) and H (residual survives where no
  ln is even needed under the 400-class... yet the comb persists). The
  POISSON-tension dissolves without it.
- **T1d (custom rational):** still dissolved; E adds NSWC-erfc1-tail,
  gratio-CF, SLATEC, Chiarella-Reichel to the tail kill list with numbers.
- **T1e (tiny = x·c):** dead a fortiori (H: no constant of any value works).
- **T1f (tail = public libm + unsplit z²):** refined — unsplit z² and per-op
  binary64 staging confirmed; libm is beaten by Cody-unsplit (3,218) with the
  family ceiling at 3,273 (GAUSS tail) / 146/355 (direct); the named-F hunt
  continues (next: NSWC double-precision DERFC1).

**The convergent picture.** Four independent lanes now point the same way:
the compiled body behaves like **double-precision code** (per-op RN53 stores:
gam1, inner cluster, tail E·F products) around **one software exp/ln whose
result is delivered as a binary64** and carries a deterministic, mantissa-
anchored, short-coherence comb of amplitude ≲0.9 dbl-ULP (C's 0.896-width
exp-frame residual = B's binade-invariant comb = A's tiny sawtooth = the
±1 teeth in D's landmark map = H's eps). The "x87 extended continuous"
reading survives only where it is observationally equivalent (F2XM1-chain
values that round to the same doubles). The single open object is that
exp/ln's exact grain.

---

## 3. Corrections to the handoff (apply before quoting it)

1. **§4.4 tooth law: RETIRED as stated.** All six quantitative items are
   aliases of the scan grids, the model constant's bits, or the bisection
   protocol (B, verified digit-for-digit). The surviving facts: residual is a
   deterministic mantissa-only comb, binade-invariant in the clean regime,
   sharp spectral lines (z-linear within a binade), aliased angles
   γ = 0.3346561 and δ = 0.0939064 per 2⁻¹⁴ m-step (true frequencies known
   only mod 2⁵²), amplitude ≈0.9 dbl-ULP pk-pk. The amplitude law
   "ε_amp·|zl| ≈ 25.7 constant" is refuted (variance identical at e=−30 and
   e=−40); A's tiny-route sawtooth (~0.7 ULP at |zl| ≈ 700) already
   contradicted its extrapolation.
2. **§4.2 "wanted mantissa" and §9.1.3: RESOLVED as a phantom.** No object
   `0x906eba8214db6c6f` exists to measure; it is the phase-average of the comb
   over the b9train-era corpus (H). The measurable constant is per-op-b64
   gam1(½) h = `0x3fc06eba8214db6b` (A, two independent reproductions).
3. **§15 row C premise stale:** b25 was first read 2026-07-18
   (`agentJ_b25_summary.json`); this swarm's read is an independent
   replication, agreeing within noise.
4. **§5.1 "single adjusted gam1/normalizer constant ±4096 scan flat":**
   annotate as staging-specific — the true constant-g ceiling under the
   collapsed tiny model is 2,836/3,158 (still refuted, by empty exact
   intersection rather than by scan flatness).
5. **§3.1 "NORMSDIST = 0.5 + GAUSS (19/22)":** the causality is inverted.
   NORMSDIST is the primary sign-split publication; GAUSS appends −0.5 (F).
6. **§2.2 production note:** `norm_cdf`'s `0.5*(1+erf(x/√2))` shape is now
   known to be the wrong wrapper *class*, not just the wrong body.
7. **Region boundaries 0.5 / 1.375 / 6:** only 0.5 is a body boundary
   (complement direction); 1.375 is a label (G); ~6 is ERF-side saturation;
   the tail flush is the PHI-class DBL_MIN rule at z ≈ 26.543/26.544 (E).

---

## 4. New hard constraints (any future graph must reproduce ALL of these)

1. Per-op-b64 gam1(½): h = `0x3fc06eba8214db6b`; g = 1+h exact in Ext80 (A).
2. Inner complement cluster RN53-staged; j first visible at x ≥ 9·2⁻⁵⁵
   (variant A) — decides the clean {e≤−27} vs elevated {e≥−26} regime split
   (B; capture P2/P3 splits variant A from fused variant B).
3. Residual comb: mantissa-only, binade-invariant (corr +0.9999 between
   e=−30/−40), aliased angles γ/δ above, exp-result-relative width
   0.896±0.02 dbl-ULP of w, bias component also exp-frame (B+C).
4. Tiny route: dyadic transport law GAUSS(2^k) = 2^k·PHI(0)-mantissa,
   k = −50..−1020, 971/971 (H); the 2,822/3,158 plateau with histogram
   {−1:170, 0:2822, +1:166}; sawtooth period ≈6 input-ULPs at 1e-15,
   absolute-locked across the input binade crossing (A).
5. P-side tooth map at the 1/8 binade: m(k) = −1 forced at
   k ∈ {0,1,4,8,29,37} and √2/8; m(k) = 0 forced at
   k ∈ {11,15,18,22,25,32,40} and 15 below-1/8 rows (D).
6. Complement direction 700/700 with ordinary RN53 subtract of the stored
   primary; flip at 0.5; no 1.375 seam; three Q channels bit-identical on
   every overlap (330/330) (G).
7. Tail: unsplit exp(−RN53(z·z)), per-op binary64 E·F, PHI-class flush;
   five F-body pin witnesses (z = 0.75 → −3.73, 1.28125 → +4.17,
   1.875 → −7.09, 2.125 → −4.56, 5.0 → −5.41, units 2⁻⁵³ rel) (E).
8. NORMSDIST wrapper G-F3 with its 64-row prediction table; GAUSS derived by
   trailing −0.5 (F).

---

## 5. Capture queue (designs only; serialized root lane executes)

All scripts in `smart-fuzzer/work/w109/erf-swarm-20260821/`, Value2
object[,] plumbing, provenance headers, none auto-run. Priority order:

| # | Script | Rows | Decides | Predicted split |
|---|---|---:|---|---|
| 1 | `Run-TinyTieSeparators.ps1` | 14+controls | G-A80 vs G-A400 (the 480-tie kill) | e.g. GAUSS(`0x02e64367549eb209`) = `0x02d1c37756a97d07` (A80) vs `…08` (A400); any third value kills both and fingerprints the internal chain at depth |
| 2 | `Run-Z8Neighborhood.ps1` | 129+17 | H-D1 vs plateau; hands B a 129-point direct tooth map | ERF.PRECISE(`0x3fc0000000000001`) = `0x3fc1f5e1a35c3b8a` (H-D1) vs `…8b` (plateau) |
| 3 | `Run-ErfToothB-FreshBinades.ps1` | 424 | P1 mantissa-invariance (alias account); P2/P3 inner-cluster variant A vs B | e=−28 ladder must reproduce the m30 eps pattern row-by-row; variant A: e=−26 breaks at row 8 (m=√(9/8)); variant B: e=−27 breaks at row 94 (m=√3). Fix the CV provenance readout (`$wb.Item_Default`) first |
| 4 | `Run-NormsdistGaussLadder.ps1` | 64 | G-F3 on provenance-rich 20228 | NS(−1) = `0x3fc44ed0bb7cb209` = half of same-sheet ERFC.PRECISE(z) vs both rivals' `…208`; NS(−37.52) = +0 with ERFC finite. Assert/record CV2 when executing |
| 5 | `Run-ComplementDirection.ps1` | 54 | 20228 replay of the 700/700 law + subtract store-site breaker | ERFC(`0x3d735c7211223903`) = `0x3fefffffffffd44f` (SSE) vs `…4e` (x87 spill); neither → direction law broken at tiny x, flag loudly |
| 6 | `Run-B26ZCross.ps1` | 8,192 | anchor-free exp-frame confirmation | miss width ×2 jump (0.505→1.011 pub-ULP) crossing z = 2⁻²⁹; no jump refutes the w-grid verdict |
| 7 | `Run-TailDiscriminators.ps1` | 24×3 | split-vs-unsplit exp; F-noise granularity; flush bisect | ERFC.PRECISE(`0x40150000012804DF`) = `0x3D3FD5F0287EFBD7` (unsplit family) vs `0x…BC8` (split family), 15 ULP apart, noise envelope ≤7 |
| 8 | `Run-GEffTightening.ps1` | — | **DO NOT RUN as written** — dyadic legs are vacuous (already in-bank). Re-scope to: 12-row window `0x3cd0000000000100..10b`, deep full-mantissa probes, ERF.PRECISE same-z cross-read | window admitting a single constant + `…52` dyadics would revive constant-g; expected: no constant, `…51` |

Free riders worth adding to any session: NORMSDIST/NORM.S.DIST columns on the
tiny-tie capture (A's script already carries them).

## 5a. Capture outcomes (same day, 2026-08-21, build 20228/x64/CV2)

The root lane authorized the batch; scripts 1–7 executed sequentially by a
capture worker (Excel process hygiene clean: 0 processes before, between, and
after; every script's own quit succeeded). Build 20228 x64, Workbook
Compatibility Version 2 — **identical to the frozen banks' reference oracle**,
so these results score directly against the prior. `Run-GEffTightening.ps1`
skipped as flagged. Outputs are new files in the swarm work dir; no frozen
bank touched. Pre-run fixes applied per §8 (toothB CV readout → the
CellRefBatch `CompatibilityVersion` pattern; NORMSDIST ladder now records
CV; both captured CV=2). All control pins fired on every script
(GAUSS(1) three independent times, PHI(0), R-pins at 1/8, NORMSDIST(0)).

| # | Capture | Verdict |
|---|---|---|
| 1 | Tiny-tie separators | **G-A400 wins 14/14, unanimously** — every separator returned the stored-z-reuse bits (e.g. GAUSS(`0x02e64367549eb209`) = `0x02d1c37756a97d08`). G-A80 (x87-continuous w-recovery with binary64 w-store) is **dead**; no third values. The surviving tie class is the 400-member stored-z family: at tiny z Excel publishes the algebraic z-reuse value — either the body short-circuits the transcendental recovery there, or its internal exp∘ln is fine enough to round back to z where host x87 microcode does not (RN53(w_x87) = z−1 on all 14). NORMSDIST/NORM.S.DIST free-riders identical to each other on every row. |
| 2 | z = 1/8 walk | **H-D1 confirmed at the landmark**: ERF.PRECISE(`0x3fc0000000000001`) = `0x3fc1f5e1a35c3b8a` = plateau−1 (plateau `…8b` refuted). Historical 1/8 pins reproduced exactly on 20228. The plateau branch-190 family is dead at the six; the P-side −1 tooth is real and directly measured. Offline map read: see §5b — all forced values confirmed; one deviation (√2/8 measures m=−2, not −1). |
| 3 | ToothB fresh binades | 424/424 rows captured (e=−28/−27/−26 ladders + offsets), CV=2. Offline read: see §5b — **P1 alias account CONFIRMED, inner-cluster variant A confirmed, variants B/C affirmatively refuted, physical z-comb refuted (P4)**; plus an unpredicted exact-integer −1 window. |
| 4 | NORMSDIST ladder | **G-F3 confirmed 64/64** on provenance-rich 20228 (eq_HF1 60/64, eq_HF2 59/64 — the rivals fail exactly at the discriminating rows). NS(−1) = `0x3fc44ed0bb7cb209` = bit-exact half of same-sheet ERFC.PRECISE(z). Falsifier row confirmed: NS(−37.52) = `+0` while ERFC.PRECISE(z) = `0x001f434e9fdf09f1` (finite, bottom normal binade) — the trailing-halving + PHI-class flush asymmetry, exactly as predicted. **The NORMSDIST/NORM.S.DIST CDF wrapper is identified** (and NORM.DIST / LOGNORM.DIST CDFs inherit via the proven 45/45 transforms). The divide-staged z control (`0x…3bcc`) correctly did NOT match. |
| 5 | Complement direction | Direction law fully intact on 20228/CV2: Q-primary 28/28 above 0.5, P-primary clean below, collapse pins at 0.5 match history, no 1.375 seam. **New store-site identification: all 4/4 subtract breakers came back x87** — e.g. ERFC(`0x3d735c7211223903`) = `0x3fefffffffffd44e` (x87 prediction; SSE `…4f` refuted). The below-half complement is `Q = RN53(RN64(1 − stored P))` — an x87 double-rounded spill, observationally equal to plain RN53 except for P < 2⁻¹². G-G1's tie class is closed. |
| 6 | b26-zcross | 8,192/8,192 rows captured, zero round-trip mismatches. Offline read: see §5b — **the w-double-GRID version of the exp frame is refuted (no ×2 jump), and so is the ln frame; the residual is exp-result-RELATIVE with a fixed scale ≈0.90·2⁻⁵³** — a scale-free relative grain, not ulp(w) quantization. |
| 7 | Tail discriminators | **Split-exp family killed**: ERFC.PRECISE(`0x40150000012804DF`) = `0x3d3fd5f0287efbdc` — 5 ULP above the unsplit-family prediction (inside its ≤7-ULP F-noise envelope), 20 ULP from the split prediction. Unsplit `exp(−RN53(z·z))` staging survives; Cody-F is not bit-exact at the separator (consistent with the characterized F-noise — the named-F hunt continues). Flush crossing narrowed: probes at 26.5433/26.5435/26.5438 all publish +0, so with the frozen last-finite at 26.543000000000003 the crossing sits in (26.543000000000003, 26.5433). |

Net new identifications from the batch: tiny-direct route is the stored-z
algebraic family (480→400 tie, transcendental-recovery class dead); the
P-side −1 tooth is real at the 1/8 landmarks; the NORMSDIST wrapper G-F3 is
confirmed on the reference build (wrapper closed, body still open); the
below-half complement subtract is an x87 RN64→RN53 spill; the tail's split-exp
class is dead on a direct separator.

## 5b. Offline reads of captures 2/3/6 (same day)

Gates: the prebuilt `check_erf190.exe` cfg-304 dump reproduced the frozen
`dump-m30.txt` bit-for-bit (256/256); an independent mpmath prec-64
replication matched the Rust dump on all 424 toothB rows. eps convention =
`toothB_parse.py`. Derived dumps and the tooth map are banked in the swarm
dir (`derived-dump-*`, `derived-z8-toothmap-m_of_k-20260821.tsv`).

**ToothB (capture 3).**
- **P1 CONFIRMED**: e=−28 tooth rows are exactly the m30 list
  [4,10,…,89,95], zero rotation shift; corr with the e=−30 pattern +0.9982
  raw, **+0.99992 under a variant-A-staged reference** — mantissa invariance
  is essentially exact. The §4.4 alias account stands.
- **P2/P3: inner-cluster variant A** (`0.5 + RN53(0.5−j)`) **confirmed**;
  variant B (fused `RN53(1−j)`, predicted break at e=−27 row 94) and
  variant C (ext outer add, row 29) both affirmatively refuted; the
  predicted variant-A signature at e=−26 row 8 (x = 9·2⁻⁵⁵, step ≈0.59)
  observed exactly.
- **New unexplained object**: exact-integer **−1 windows** — all rows with
  x ∈ [2.203·2⁻⁵⁴, 4.5·2⁻⁵⁴) sit exactly −1.000 published ULP below the
  comb, contiguous across the e=−27/−26 ladders and ending exactly at the
  variant-A visibility threshold 9·2⁻⁵⁵; plus an extra −1 at each ladder's
  boundary row 98 (−2.0 total), a displaced tooth (34→37) at e=−26, and a
  smooth drifting bias in the elevated regime. No proposed staging predicts
  these windows; they are the sharpest new body constraint from the batch.
- **P4: physical z-comb refuted** — interleaved half-step grids show two
  independent alias patterns (phase difference bimodal at exactly the
  complement of frac(g·2⁴⁴) = 876/2048); teeth do NOT share z positions
  across grids.

**b26-zcross (capture 6).** Measured across the z-binade crossing at 2⁻²⁹:
width 1.026 → 1.014 pub-ULP (ratio 0.99, **no ×2 jump**), exact rate
74.3% → 74.3%. The w-double-GRID quantization story is refuted — and the ln
frame stays refuted too (e30→e20 ln-transfer fails ~3×). What survives and
sharpens: **W/m_ans is frame-constant at 0.91/0.90 across the crossing — the
residual is exp-result-relative with a fixed RELATIVE grain ≈0.90·2⁻⁵³**,
i.e. a scale-free relative perturbation of the exp result (the b25/b18 cells
could not separate grid from relative because their w-mantissa was
corpus-averaged; b26 pins m_w at 2.0 vs 1.0). The e=−20 leg carries the
known extra coherent component (widths 1.61/1.51, lag-1 autocorr +0.25/+0.15)
and is reported separately.

**z=1/8 tooth map (capture 2).** 146/146 rows joined; m-histogram
{−2:3, −1:32, 0:105, +1:6}. All forced values confirmed (m=−1 at
k∈{0,1,4,8,29,37}; m=0 at k∈{11,15,18,22,25,32,40}). **Deviation: the √2/8
row measures m=−2, not the forced −1** (Excel `0x3fc944d158b76b61`; H-D1's
alternative hit 6/6 ladder landmarks but missed s6). Structure: a 15-wide
central megatooth m=−1 on k∈[−4,+10]; strongly asymmetric (below-1/8 rows
have NO −1 teeth, only sparse +1 at k = −58, −49, −33); post-megatooth tail
spacing ≈8.3k, consistent with Agent D's per-op-53 stored-z·g period class
(8.15k) though not its simple duty. Cross-surface coherence perfect:
ERFC = RN53(1−P) 146/146, legacy ERF ≡ ERF.PRECISE 146/146,
CHIDIST(2z²,1) ≡ ERFC 146/146; the GAUSS helper columns are fully explained
by the wrapper's argument round-trip (z′ = z+{0,1,2} ulp), G-F3-consistent
145/145 — one-body thesis intact at ulp resolution.

Open after the batch and reads: the body's relative-grain exp/ln object
(now with the −1 windows, the megatooth map, and the 0.90·2⁻⁵³ grain as
hard constraints), the √2/8 m=−2 outlier, the named tail F, and the
re-scoped g_eff window capture.

## 6. New oracle without a capture

`answers-b24-normref.json` (16,495 NORM.S.DIST rows, all-negative x down to
−36) is, under G-F3, an **implied-Q bank**: Q = 2·NS exactly (mantissa
preserved) at 16,495 fresh z in [0.035, 25.5] — zero overlap with every
existing ERF/ERFC bank, sampling the tail far beyond any erfc capture. Caveat:
the file embeds no build/CV provenance (same class as the historical
WitnessSets); treat as strong historical evidence pending ladder #4. Agents
D/E-class work should mine it next.

## 7. What was killed this session (add to the §5 catalog)

- The §4.4 tooth-law constants as generator signatures (grid/protocol alias).
- T1c ln-residual on the 190-path; any zl-lattice / stored-zl mechanism.
- The Ext80-continuous inner complement cluster.
- Any single-constant g_eff for the tiny route (all 20 public mixed-spill
  gam1 values, g_x, CR53/CR64(2/√π), fdlibm efx+1, R(0⁺) — empty exact
  intersection); the "measurable gam1 Ext80 mantissa" as an object.
- Stored-z² binade-bottom artifact as the six-landmark mechanism.
- NSWC/CDFLIB erfc1 tail branches, gratio a=½ CF, Cephes, SLATEC,
  Chiarella-Reichel/Ooura, extended-product delivery — on tail rows.
- H-F1 (`0.5+GAUSS`) and H-F2 (P-side) as the NORMSDIST wrapper.
- Cody XBIG hard-zero (again); split-argument exp (again, now at ~100×
  amplification in the flush band).

## 8. Hygiene (root lane attention)

1. **Seal hazard — DEFUSED 2026-08-21:** `smart-fuzzer/work/w109/G3-01-dist/agent_erf_normalized_race.py`
   (pre-existing) auto-loaded `answers-b9heldout.json` when present — and it is
   present. No swarm agent ran it. The loader now skips the sealed file
   (work-dir-local fix; a repo-wide grep found no other code path naming it).
2. `Run-ErfToothB-FreshBinades.ps1`: fix the CV provenance readout before use.
3. `Run-NormsdistGaussLadder.ps1`: assert Workbook Compatibility Version 2 on
   the fresh workbook when executing.
4. `Run-GEffTightening.ps1`: re-scope per §5 row 8 before use.
5. Minor verifier-noted slips retained in the per-agent records (A: po2 family
   spans fields 1..973 in the direct route; E: ceiling 146/355 and max
   residual +4.17; H: 8-of-12 window splits, pred_g_dyadic constant unnamed).
6. Capture-file hygiene (from the offline reads): `answers-toothB-fresh.json`
   carries a UTF-8 BOM (serde rejects it); `answers-b26-zcross.json` has
   doubled `0x0x` bit prefixes and its embedded provenance records
   `cv=False` (CV was not read by that script — the session's other scripts
   verified CV=2 on the same Excel instance; build 20228 is embedded).
   Sanitized copies were used for scoring; originals untouched. Normalize
   before any promotion-grade use.

## 9. Artifacts

- Capture scripts + data: `smart-fuzzer/work/w109/erf-swarm-20260821/`
  (8 Run-*.ps1, `agentD_z8_predictions.tsv`, `agentD_decoded_q.json`,
  `agentG_subtract_breakers.json`, `agentH_geff_capture_rows.json`,
  toothB analysis scripts, agentC b25 gate/read scripts)
- New tracked racer: `smart-fuzzer/tools/calc_graph_racer/src/bin/agentA_tinytie.rs`
  (hardware answer-key generator for the 14 separators)
- Full agent+verifier records (headline, computed results, spot-checks,
  proposals): session workflow output; per-agent extracts were reviewed and
  the load-bearing numbers are reproduced in this document.

## 10. Production landing (same day, subsequent session)

Landed the identified G-F3 NORMSDIST wrapper and derived GAUSS, including
the stored-z G-A400 tiny-direct route, on the still-open ERFC.PRECISE body.
Record: [`W109_NORMSDIST_GF3_WRAPPER_20260821.md`](W109_NORMSDIST_GF3_WRAPPER_20260821.md).

This is the CHIDIST(df=1) pattern: the public graph is now what production
computes; leftover ±1 ULP at `NORMSDIST(-1)` / `GAUSS(-1)` is the ERFC body
at `z = RN(1/√2)` (same witness as `CHIDIST(1,1)`). `GAUSS(1)` moved from
2 ULP (`0.5*libm::erf`) to 0 ULP because `1-0.5*Q` absorbs that body ULP.
Inverse surfaces were kept on `erf_based_cdf` so INV bit pins do not ride
the open body.

Not a function-phase-complete claim. Body, tiny comb/grain, and sealed
heldouts remain open.
