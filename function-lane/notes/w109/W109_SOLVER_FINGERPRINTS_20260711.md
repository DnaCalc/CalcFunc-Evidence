# G6 solver phase — guess-sweep fingerprints (2026-07-11, build 20131)

Corpora: answers-irr-r0.json (49), answers-rate-r0.json (48).

## IRR (cashflow A = [-1000,300,420,680]; B = [-1000,1210])

- Case A: 24 guesses -> 18 distinct published values spanning ~7.8e-12
  absolute (~7800 ULP at 0.1634). Publication is tolerance-gated, NOT
  converged-to-fixpoint; the final iterate depends on the guess.
- Case B: every guess (incl. -0.5, 1.5) lands within +-8 ULP of the exact
  double root 1210/1000-1 = 0x3fcae147ae147ae0, and the outputs take only
  THREE values: root, root+8 ULP, root-8 ULP. guess==root publishes the
  root bits unchanged -> NO mandatory seed perturbation for IRR (unlike
  the RATE root==guess 72-ULP recon witness).
  The 8-ULP quantization of the last step is a strong schedule
  discriminator (last update lands on a coarse grid -> the update term is
  computed at ~1e-16 absolute from a tolerance-scaled quantity).

## RATE (A = (10,-120,1000,0,0); B = (360,-599.55,100000,0,0))

- Case A: 22 distinct outputs over 24 guesses (same loose-tolerance
  publication shape as IRR-A); guesses -0.5/-0.3 -> #NUM!.
- Case B (root 0.0049999932): #NUM! from guesses {-0.5..0.0, 0.5..5.0} —
  divergence from guesses as benign as 0.5 despite a well-behaved f.
  Plain Newton would converge from 0.5 in <10 iterations -> the update is
  NOT plain Newton (secant with the documented 20-iteration / 1e-7 cap is
  the leading hypothesis; docs: "if results do not converge to within
  0.0000001 after 20 iterations, RATE returns #NUM!").

## Next

1. Feed published outputs back as guesses (fixpoint probe): if returned
   unchanged, the stop test is on the INPUT residual/step, pinning the
   tolerance form.
2. Dense guess ladders around plateau boundaries (e.g. IRR-A between
   0.09 and 0.095) -> exact tolerance constants via threshold bisection.
3. Solver-VM grid in calc_graph_racer (iterate-node): method {newton,
   secant, damped} x seed rule x tol type {|f|, |dx|, |dx| relative} x
   tol value {1e-7 ladder} x cap {20, 100} x publication {last, previous,
   first-satisfying}; score jointly on IRR-A/B + RATE-A/B sweeps.
4. Prerequisite kernels: IRR f = NPV polynomial (race spill vs plain on
   the SAME published data via f(published) residual fingerprints in MPFR);
   RATE f = annuity equation (W108 Phase C characterization exists).
5. YIELD/ODDFYIELD after RATE/IRR (100-iteration price inversion; forward
   PRICE kernel already aligned).

---

# Round 2 (same day): IRR update rule IDENTIFIED from the one-step error map

Probes: bit-level guess ladders at anchor+-2^j ULP, j=24..40, both cases
(answers-irr-r1.json, answers-irr-r2.json; 128 more live rows).

## The measurement

For case A (4 cashflows) the one-step error map is PURELY LINEAR and
sign-preserving over three decades: err_out/err_in = +7.40e-7 constant
for err_in in [1e-9, 3e-5] (plateau 7.38-7.41e-7, both sides). For case B
(2 cashflows) the map is EXACTLY ZERO everywhere (every ladder guess ->
exact root bits).

## The identification

The unique model consistent with both:

- Excel iterates in v = 1/(1+r) (discount-factor space). Case B's NPV is
  LINEAR in v -> any chord/FD slope is exact -> lambda = 0. Bit-confirmed.
- The update is forward-difference Newton with RELATIVE step h = 1e-6*v:
  predicted lambda = (f''_v / 2 f'_v) * 1e-6 * v* = 7.3865e-7 for case A
  vs measured 7.40e-7 +- 0.02. (Analytic Newton = quadratic map: ruled
  out; fixed-h FD, secant seed pairs, r-space FD: all ruled out by the
  case-B zero and/or the sign/linearity of the map.)
- Publication is r = 1/v - 1 from the final v: predicts output
  quantization of ~5.86 r-ULP per v-ULP; observed case-B outputs take
  only {root, root+-8 ULP} from far guesses, and the whole ladder basin
  collapses to exact root bits.
- Stop: guess passthrough when computed f rounds to zero (observed at
  anchor+8 exactly); otherwise |dv|-tolerance around 1e-5 with the final
  sub-tolerance step still applied (apply-last), then iterate-to-fixpoint
  behavior for far guesses. Exact tol/cap/order still open.

Python plain-double simulation of this structure already reproduces
104/177 rows (all fixpoint-attractor rows) with NPV in sequential
v-accumulation form; the residual far-guess scatter (~1e2 r-ULP) is
f-evaluation staging noise -> the remaining work is the joint (small)
race of NPV staging {plain, x87-spill; seq/Horner/pow} x {h sign, tol,
cap, check order} in the Rust racer with x87 ops. Work-dir scripts:
irr_schedule_race.py, irr_vspace_race.py.

RATE contrast: no passthrough anywhere (published anchors move by
50-160 ULP when fed back) -> RATE has a different schedule (mandatory
second seed / always-step), consistent with the recon root==guess 72-ULP
witness and the #NUM! divergences.

## Round 3: expanded staging race + miss anatomy (same day)

Extended check_irr_schedule.rs axes: dv association {f0*h/den, (f0/den)*h,
fused update}, staged v-update / v+h / publication association
{1/v-1, (1-v)/v}. Winner unchanged at 112/177
(spill/horner, h=1e-6*v, tol=1e-7, apply-last, dv=f0*h/den, pub=1/v-1).

Miss anatomy (the useful part):
- ladder-B 70/72 (misses only the two 2-cycle quirk rows, -8 ULP);
- ladder-A 25/54, misses almost all exactly +-8 r-ULP = ~1.35 v-ULP;
- the j~40 rungs: Excel stops after ONE step where tol=1e-7 takes two
  -> the true stop rule is still not a plain |dv| threshold (no single
  tol explains one-step-at-9.5e-7 AND multi-step far sweeps; candidate
  forms to test: |dv| vs h comparison, |f|-based with staging-true f,
  fixed-step-count-after-bracketing);
- sweep-A 3/24: far trajectories amplify any staging mismatch
  chaotically; they close only after the kernel is bit-exact.

Diagnosis of the +-8 scatter: den = f1 - f0 is a catastrophic
cancellation of two ~O(0.001) values carrying ~4.4e-13 absolute NPV
noise -> ~2.3e-10 relative error in dv -> ~1.5 v-ULP in the update ->
+-8 r-ULP after publication. So the remaining unknown is the exact NPV
evaluation chain (association/order variants beyond seq/horner, the
v+h formation, and h = v*1e-6 vs v/1e6), NOT the schedule skeleton.
Next: enumerate NPV forms against the ladder-A one-step rows alone
(they isolate a single FD step), then revisit the stop rule with the
winning kernel.

## Round 4 (2026-07-12): h = 1e-3 absolute, two-step composition; NPV probed directly

The Act-IV one-step reading was itself an over-fit: a single FD step's
error ratio must grow ~25x across the ladder (quadratic term), but the
data's ratio is nearly constant. The unique fix: the ladder rows take
(at least) TWO steps, and lambda_total = lambda'^2 with lambda' =
0.8593 * h  ->  h = 1e-3 ABSOLUTE in v ((0.8593e-3)^2 = 7.39e-7 = the
measured plateau). Python race confirms: h=0.001, always >=1 applied
step, |dv| < tol (1e-7..1e-10 degenerate) with apply-last -> 110/177 in
plain double; the multi-step Rust mask fit reaches 129/229 after adding
52 mid-ladder probes (j=41..53, answers-irr-r3.json), then 132/229 with
a DIVISION-form NPV (t /= (1+rate)) and NEGATIVE probe step.

Case-B mid-rung +-8 misses quantified the residual: the landing offset
scales like f0's own cancellation noise (~1.4e-13 relative), and NO
staging of s = 1210*v - 1000 reproduces Excel's realization -> the f
kernel is not a v-polynomial. Probed worksheet NPV directly (94 rows,
answers-npv-r0.json; IRR's f is documented as cf0 + NPV(rate, rest)):
- every 1-flow row matches the division form exactly;
- best 3-flow form: REVERSE Horner division chain s = (s + c)/w from the
  last cashflow (79/94, mask: sum stored, division extended, w stored);
  15 rows remain at +-1..2 ULP.

Next: widen NPV probe shapes (n=2,4..8 flows) to pin the chain
associativity, close the kernel, then re-run the solver fit with the
identified f (the schedule skeleton h=1e-3/two-step/tol is settled).

## Round 5 (2026-07-12): RATE joins the harness; annuity kernel identified 96/96

NPV kernel stalled at 106/142 (nine forms x 16 masks, +-1..2 ULP residue
on a quarter of multi-flow rows) -> pivoted to RATE per plan.

RATE ladder (45 live probes, answers-rate-r2.json):
- lambda-plateau +3.48e-5, sign-preserving, over j=22..34;
- stop boundary between j=34 (err 6.7e-8) and j=36 (2.7e-7): the
  documented |dv| < 1e-7 tolerance, apply-last;
- inverting the plateau through the annuity curvature (f''/2f' = 5.900
  at the root): two-step h = 0.00099981... = 1e-3 ABSOLUTE.
  **Same h = 1e-3, same two-step near-root composition, same 1e-7-class
  stop as IRR: a shared FD-solver harness** (IRR iterates v = 1/(1+r),
  RATE iterates r; each linearizes its own f's natural argument).
- No passthrough anywhere; the attractor is fuzzy (+-100 ULP f-noise,
  consistent with the annuity kernel's larger evaluation noise).

FV / annuity kernel (96 direct worksheet FV probes, answers-fv-r0.json;
8 shapes x 12 rates incl. type=1 and n=360): fit_fv_stores.rs reaches
**96/96 bit-exact**: FV = -(pv*P + pmt*(1+rate*type)*((P-1)/rate)) in
PLAIN DOUBLE with P = (1+rate)^n via LSB-first binary exponentiation
(stored steps). Free bits: P/sum stores (degenerate); type-factor
association tie {pmt*(tf*q), q*tf folded, w-shift} needs one
discriminating probe. Closure discipline still pending (held-out +
adversarial: tiny rates, negative rates, huge n) before promotion, but
this kernel underpins G6-01 (PMT family) and RATE's f simultaneously.

Cross-pollination note for the NPV residue: the annuity kernel is
plain-double binexp — the IRR NPV per-term discount may likewise be a
plain binexp POWER per term with a c*recip(P) or c/P association not yet
in the form set.

## Round 6 (2026-07-12): the wide annuity surface — FV and PV closed, PMT resists

150 new live rows (answers-fv-r1 / answers-pmt-r0 / answers-pv-r0):
FV adversarial+held-out (rates 1e-15..745, negative, n=500, type=1) and
wide PMT/PV discovery grids. The kernel is plain double, so Python is
bit-faithful; results (annuity_family_race.py):

- **FV: 149/149 over the FULL corpus** (discovery + adversarial +
  held-out): FV = -(pv*P + pmt*(tf*q)), P = binexp LSB-first(1+rate, n),
  q = (P-1)/rate, tf = 1+rate*type; rate==0 -> -(pv+pmt*n).
  The earlier "type-factor tie" is an algebraic degeneracy (tf == w
  bit-for-bit at type=1; tf*q commutes) — the kernel is unique.
- **PV: 48/48 first race**: PV = -(fv + pmt*(tf*q))/P, same kernel.
- **PMT: best 21/48** across 15 plain-double compositions AND
  platform-pow P variants (misses +-1..5 ULP) -> PMT does NOT share the
  plain-double path; next: x87-spill staged race (Rust) over the same
  composition zoo.

Consequences: G6-01 (PMT family) now has two of its members identified
bit-exactly on first corpora; RATE's f is the closed FV kernel;
remaining G6-01 work = PMT (+IPMT/PPMT/CUM* compositions after PMT).

## Round 7 (2026-07-12): PMT staging race opened

fit_pmt_stores.rs: composition zoo {direct, split, (num/(P-1))*(rate/tf),
rate-mul, reciprocal, PV-dual} x P-forms {binexp, loop-multiply, stored
CRT pow, EXTENDED x87 pow chain} x 512 store masks. Leader: extended x87
pow chain + comp (num/(P-1))*(rate/tf) at 34/48. Diagnostics: ordinary
rates miss +-1..7; rate=1.5e-6 rows swing wildly (up to 16285 ULP off
under the leader) -> PMT's small-rate path is materially more accurate
than any current variant: suspect a dedicated (P-1) formulation
(extended chain into the subtraction, or expm1-style) or a different
inversion. PMT does NOT reuse the closed FV/PV plain-double path.
Next: probe PMT vs FV/PV at identical (rate,n) to difference the paths
directly; then IPMT/PPMT once PMT lands.
