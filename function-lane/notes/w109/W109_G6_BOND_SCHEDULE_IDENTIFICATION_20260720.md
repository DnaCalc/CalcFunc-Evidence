# W109 — G6 bond-schedule identifications (2026-07-20)

Cluster push after the G3-01 BINOM landing. Two lanes opened the same day;
both cracked at the SEMANTIC level within hours by exact-constraint methods
(single-witness hypothesis first, lattice capture second, bit-race third).
Work dir: `smart-fuzzer/work/w109/G6-b2b3/` (gitignored). Agents: agent-V
(PRICE staging + landing), agent-W (ACCRINT identification).

**2026-08-09 ACCRINT closure note:** the July ACCRINT narrative below is kept
as identification history, but its 13-row open-publication conclusion is
superseded. Commit `cd1f9fe` identifies and lands the final stored-coupon by
stored-accrual-fraction x87 publication multiply; retained and fresh evidence
now replays `146,850/146,850`. BUG-FUNC-030 is `closed_signed_off`, and G6-02
is retired. PRICE, DURATION/MDURATION, YIELD, PMT-family, and other catalog rows
remain separate open lanes, so the wider report and W109 campaign stay
`scope_partial`.

## Lane A — G6-03d: PRICE at Actual/360 & Actual/365 (material, ~cents)

**Identity: Excel's PRICE derives the settlement discount fraction with a
UNIVERSAL rule `dsc = E − A`** — it never counts days settlement→next-coupon
directly.

- `E` = coupon period length by basis: `360/f` (bases 0, 2, 4), `365/f`
  (basis 3), actual days (basis 1).
- `A` = accrued days PCD→settlement by basis (actual for 1/2/3, 30/360 for
  0/4).
- On bases 0/1/4, `E − A` coincides with the direct count (except
  settlement-on-the-31st 30/360 rows — where `E − A` is ALSO the fix), which
  is why the rule stayed invisible: it only diverges on Actual/360 and
  Actual/365, where `E` is a fiction (180 / 182.5) and `A` is real days.
- First-try witness check: `PRICE(2020-09-20, 2025-01-01, .06, .03, 103, 2,
  basis 2)`: off = (180−81)/180 = 0.55 → 114.588731 = Excel's 114.5887
  (OxFunc/faithful-formula: 103/180 → 114.550379, 3.8 cents low).

**The oracle disagrees with itself:** Excel's published `COUPDAYSNC` returns
ACTUAL days (103) at bases 2/3 on the same arguments — 458/458 captured rows
at each of bases 2/3 have `pub ≠ E−A`, while all 144 basis-0/1/4 rows have
`pub == E−A`. PRICE's internal DSC is not COUPDAYSNC. (OxFunc's COUP*
functions were never the problem.)

**b37 battery** (7,472 PRICE rows: bonds BE mat 45658 r.06 red103 f2 /
BL mat 45717 r.045 f2 leap-Feb period / BQ mat 45658 r.08 f4; settlement
day-ladders × 8 yields × bases 2,3 + sparse 0,1,4 controls; plus 6×1,060
COUP* rows). Four-variant race (`race_b37.py`, plain-double emulation):

| variant | b2 exact | b3 exact | b0 | b1 | b4 |
|---|---|---|---|---|---|
| direct-dsc / powf | 0/3664 | 0/3664 | 43/48 | 46/48 | 43/48 |
| direct-dsc / binexp | 0/3664 | 0/3664 | 45/48 | 48/48 | 45/48 |
| **e−a / binexp** | **3474/3664** | **3446/3664** | **48/48** | **48/48** | 45/48* |

\* the 3 b4 misses are the emulator's day-count shortcut (US 30/360 used for
European dates), not Excel. Residual after the semantic fix: ±1..4 ULP
staging micro-detail (~190 b2 + ~218 b3 rows) — agent-V racing (fractional
pow realization, per-op x87 DR staging, summation order), then landing
`dsc = e − a` in `pcomp_disc` + fresh b38 held-out gate.

Direction of error vs the F# ExcelFinancialFunctions lineage: EFF (and
OxFunc's faithful port) implements the DOCUMENTED quantity (actual DSR);
Excel's ATP implements the derived one. Same porting-hole pattern as
msvcr100's missing expm1/log1p: the published description is not the code.

## Lane B — G6-02: ACCRINT calc_method semantics (material, was "1 ULP")

The catalog row said one 1-ULP witness. The b39 lattice (25,410 rows: bonds
W/Q/A/E, settlement every 3rd day across ~2.5 periods, bases 0-4, rates
.05/.037/.0615, par 1000/997.5, calc_method both) says the row was hiding a
semantic divergence:

- **Excel calc_method=FALSE is the LEGACY FLAT computation**: one fraction,
  no period structure — `a = days(issue→settlement, by basis) / canonical`,
  result `par·rate/f·a`. Verified e.g. W bond settlement 43833 basis 2 par
  997.5: Excel 37.129167 = 24.9375·(268/180), 268 actual days issue→settle.
- **Excel calc_method=TRUE = the period-aware walk** (partial + 1.0 per
  whole period + tail partial) — what OxFunc implements for TRUE.
- The two are bit-identical on 7,752/12,705 captured pairs (pre-first
  regime, and 30/360-aligned post rows where flat ≡ sum), differ by ±1-2 ULP
  on staging elsewhere pre-first, and split MATERIALLY post-first on actual
  bases (4,227 pairs, e.g. 268/180 flat vs 84/180+1 walk).
- **OxFunc's FALSE (accrue from one period before first) matches NEITHER**
  — production scores 17,967/25,410 with ~6,100 material calc=FALSE rows.
- Remaining sub-classes for agent-W: ±1-2 ULP staging both paths (~1,100
  rows); a material 219-row TRUE-path class on bond Q (quarterly, basis 1,
  post-first) — suspect canonical/period handling; several 3-row
  (settlement × 3 rates) boundary groups.

Production scorer: `check_accrint` bin (calc_graph_racer). Residual bank:
`b39_resid.json`.

## Method note (for the ledger)

Both lanes cracked on the SAME move: treat the single catalog witness as an
exact equation, hand-test the 2-3 structurally distinct conventions against
it in plain arithmetic BEFORE capturing anything, then confirm the winning
hypothesis at the bit level on a lattice. The b37/b39 lattices were designed
AFTER the hypothesis, as confirmation + staging instruments, not as search
corpora. Contrast with the G3 walls, where the op-graph family is genuinely
outside parametrization — here the divergences were one source line each
(`dsc = e − a`; flat-vs-walk behind `calc_method`).

## Lane A — LANDED + GATED (2026-07-20, agent-V)

Staging identification on top of `dsc = e − a`:

1. **Fractional discount pow = the x87 CRT chain** `exp(RN53(RN64(y·ln x)))`
   — byte-identical to production `excel_numeric::excel_pow_chain`, i.e. the
   SAME pow recovered independently in the G3 lane-1 distribution-substrate
   work. Cross-lane confirmation, verified against hardware `x87_serve`.
   Alone lifts b2 3474→3656, b3 3446→3658.
2. **Body = plain single-rounded double**, coupons ascending + separate
   redemption term. Refuted (b2+b3 exact of 7,328): sep+powf 7,120; folded
   redemption 5,117; reversed 6,493; extended-accumulator family 4,665-5,500;
   reciprocal-multiply 4,817; x87-per-op-DR body worse. Winner sep+x87chain
   7,314 (emulator), production 7,458/7,472 overall.

Landed: `pcomp_disc` `dsc = e − a` (universal, all callers);
`excel_bond_pow` fractional branch → `excel_pow_chain` (PRICE-only via
`binexp=true`). Pins `price_dsc_e_minus_a_and_x87_pow_chain_pins` (catalog
witness `0x405ca5adc69c74fb`, basis-3 sibling, settle-on-31st basis-0, pow
discriminator). Full suite 1,510 green, zero pin movement, YIELD pins
byte-stable. **Fresh b38 held-out: 945/945 across all five bases** (5 new
bonds, month-end/leap/n=1/extreme-yield). Coordinator re-ran the gate +
suite independently — reproduced.

Open residual (NOT accepted): 14 extreme-yield rows ±1 ULP
(`agentV_residual14.json`, with 250-bit true-sum bits per row — Excel's
published value sits up to +3 ULP ABOVE the correctly-rounded true sum, an
accumulation op-graph fact). Next probe: adjacent-double yld bracket +
truncated-ladder partial sums (battery b41). Blast radius: DURATION now
inherits the `E−A` dirty on bases 2/3 (its own open lane G6-03c); YIELD
unchanged on its pinned witnesses.

Canonical agent record: `smart-fuzzer/work/w109/G6-b2b3/agentV_results.md`.

## Lane B — ACCRINT graph-identification history (2026-07-20, agent-W)

July body model (the later final-publication result below narrows the old
"all plain SSE2" statement):

1. **calc_method=FALSE = flat fraction + WHOLE-PERIOD SKIP.** For issue
   inside the canonical period: `days(issue→settle)/canonical`. For issue in
   an EARLIER coupon period: stub `[issue, B1]/L_issue` + `[pcd, settle]/
   canonical` as two divisions summed — every whole grid period between B1
   and pcd contributes NOTHING. Consequence Excel faithfully publishes:
   accrual is NEGATIVE when settlement < pcd (pinned in the regression
   test). The b40 gate falsified the first version of this rule (remainder
   measured from B1, not pcd) — exactly the under-determined corner the
   battery was designed to expose; the skip-rule revision then passed the
   fresh b42.
2. **calc_method=TRUE = period walk summed BACKWARD** (settlement side
   first; forward accumulation is 1 ULP off on ~9% of rows). Interior whole
   periods = 1.0; act/act issue stub by its own actual length; the
   settlement-side period is ALWAYS days/canonical, even when settlement
   lands exactly on a coupon date.

Historical pre-publication-closure gates (coordinator-verified on the
production kernel via check_accrint):
b39 ident 25,407/25,410; **b40 fresh 51,417/51,420; b42 fresh
68,783/68,790** — combined 145,607/145,620 (99.991%). Suite 1,511 green,
zero pin movement (the historic BUG-FUNC-030 leap-Feb pin was a true Excel
witness and survived unchanged). Landed: `accrint_kernel` rewrite +
`issue_period_grid` helper + `accrint_staging_bit_exact_vs_excel_w109`
(8 live pins incl. the negative-accrual skip witness and a c0/c1 1-ULP
pair).

Historical residual at this checkpoint (subsequently closed below): 13
bistable rows across the three corpora,
ALL at rate 0.0615 — perfectly rate-selective across bonds, bases,
calc_methods, and regimes. The flip therefore lives in the
`par·rate/f`/publication last-bit staging, not the day-count layer.
Next probe: b43 rate ladder 0.0615 ± k·ulp on the flagged bonds.
Canonical agent record: `smart-fuzzer/work/w109/G6-b2b3/agentW_results.md`.

## Lane C — G6-03c DURATION/MDURATION: LANDED + GATED (2026-07-20, agent-X)

Identity: `off = (E−A)/E` (shares PRICE's derived schedule — the docs-era
kernel weighted with the DIRECT settlement→next span while dividing by the
E−A dirty, a mixed state that put bases 2/3 at 0/1272); discount =
`excel_bond_pow` (the PRICE substrate); Macaulay body = plain-f64 SSE2 with
redemption separate, weights grouped `(diff·cash)/disc`, publication
`num/den/f` over its OWN sums. Accrued span A = CoupDaysBS
`diff360_us(prev, settle, ModifyStartDate)`, NOT plain `us_30_360`: the two
differ only on 31st/month-end settlements by adjustment ORDER (a 1-integer A
difference ≈ 2.5e13 ULP of duration).

The gates earned their keep AGAIN: the b45 pre-registered gate (456/540)
exposed the month-end A-convention break that b44 could not see; the fix is
one line; the fresh month-end-majority b46 then gated clean — DURATION
641/720 exact / all misses ±2 / zero material, MDURATION 644/720 mirroring
exactly (the `/(1+yld/f)` staging is validated). b44 final 6217/6360.
Suite 1,609 green, 8 pins added (both former catalog witnesses now exact).

Open residual (NOT accepted): the off-coupon ±1-2 ULP class
(`agentX_b44_residual143.json`, symmetric {−2:14, −1:59, +1:56, +2:14}) —
the SAME shared fractional pow-chain wall PRICE left open; one cross-lane
probe (b41/b43 family) covers both.

At the July checkpoint, three same-day landings came from one cluster: PRICE
(b38 945/945), ACCRINT
(b40+b42 145,607/145,620), DURATION/MDURATION (b46 641+644/720 ±2). Every
lane followed hypothesis-first → lattice → pre-registered held-out gate,
and TWO of the three had a wrong sub-rule caught only by the gate.

## b43 probe — historical 0.0615 discriminator (2026-07-20, coordinator)

Rate-ULP ladders (0.0615 ± 32 ulps × the 12 unique bistable rows, 780 live
rows): **the flip is ISOLATED at exactly the double nearest 0.0615 — all 64
neighbors bit-exact on all 12 ladders.** A staging difference would flip in
bands or scattered points; an isolated single-input flip recurring across
different bonds/dates/calc-paths is a TIE/publication phenomenon. Second
selector: all 13 rows are basis 3 (canonical 182.5) or basis 1 (actual) —
never 0/2/4 — so the fractional/irregular divisor is a co-condition.
Refuted on-row: 15-significant-digit publication snap (4/12, and the
failures go the WRONG WAY — ours is the short decimal, Excel's the
neighbor); naive DR-final-multiply and DR-coup-chain (0/12, but the probe
reconstructed `a` circularly from our own result — REDO with the model's
exact day-count quantities before trusting this refutation).
NEXT PROBE (banked, offline-ready): recompute each row's exact `a` from
agentW_model2.py quantities, race {SSE2, DR-final, DR-all, extended-a}
variants at 250-bit reference to find which op hits a 53-bit tie at exactly
the 0.0615 double; then a par-ladder (997.5 ± k·ulp) to separate
rate-tie from product-tie. Corpus: batch/answers-b43-accrint.json.

## Lane B final closure — exact ACCRINT publication graph (2026-08-09)

The exact current-reference calculation graph preserves the July day-count and
accrual-fraction programs, but corrects the final publication boundary:

```text
coupon = (par * rate) / frequency        # ordinary f64, stored
a      = identified accrual fraction     # ordinary f64, stored
result = excel_x87_mul(coupon, a)         # RN53(RN64(coupon * a))
```

This is a one-node correction to the July body classification. The
`calc_method=FALSE` flat/whole-period-skip fraction and `calc_method=TRUE`
backward walk stay in ordinary binary64, as does coupon construction. Only the
final multiplication of the two stored values uses the x87 PC64 operation and
binary64 publication store. The old plain-f64 final multiply explains all 13
residual rows without changing the already identified schedule graph.

The repair and exact discriminator pins landed in `cd1f9fe`.

| Corpus | Exact production replay |
|---|---:|
| b39 identification | `25,410/25,410` |
| b40 held-out | `51,420/51,420` |
| b42 held-out | `68,790/68,790` |
| b43 rate ladder, recaptured | `780/780` |
| fresh frozen publication held-out | `450/450` |
| **Combined** | **`146,850/146,850`** |

The current-reference sign-off sets were captured through Excel 16.0 build
20228 x64, workbook Compatibility Version 2, `Run-W109BulkBatch.ps1` with
`-NoCache`, and `cell_value2_bulk` plumbing. The recaptured b43 answer SHA-256
is `CE2CB4B34FD46DEE40DDCD4724769471F255BA2ECE81D957546BA079D4CDF847`;
the fresh held-out answer SHA-256 is
`D0A6F58585AAE4E8C5727FD0EE5E792B686E970FF1B721B6D1CBD257C301B58C`.
The focused exact pin passed `1/1`; the post-patch full core run passed `1519`
library tests with `0` failures and `4` ignored tests, plus all integration and
doc-test targets.

Status axes for G6-02 only:

- `execution_state: complete`
- `scope_completeness: scope_complete`
- `target_completeness: target_complete`
- `integration_completeness: integrated`
- `open_lanes: []` within G6-02. The wider bond/financial family, other catalog
  rows, alternate profiles, and global W109 audit remain open.

The scoped `OPERATIONS.md` Sections 12 and 14 audit is recorded in
`BUG-FUNC-030_accrint_accrued_interest_half_value.md` and passes. The existing
BondCoreFamily Lean binding/formal substrate is unchanged; the preceding W109
Lean build passed `492` jobs. No FEC/F3E boundary or evaluator-facing clause
changed, so no cross-repo handoff is required.

---

# Lane D — PMT / annuity ring (G6-01), 2026-07-21 (coordinator, Opus)

The financial-time-value ring (PMT/PV/FV/IPMT/PPMT/CUMPRINC) attacked with the
**metamorphic-sibling method** on the disjoint 875-row held-out corpus
(`answers-pmt-heldout.json`) + the 48-row r0. New tooling:
`tools/calc_graph_racer/src/bin/race_pmt_substrate.rs`, `race_pmt_x87stable.rs`;
`work/w109/G6-solvers/pmt_combine_search.py`, `gen_pmt_meta.py`, `pmt_meta_test.py`.

## Finding 1 — FV/PV and PMT use DIFFERENT algorithms (metamorphic proof)

`annuity_family_race.py` (re-run): **FV var0 = 149/149 and PV var0/var2 = 48/48
bit-exact** with the *naive FORWARD* binexp kernel in **plain SSE2 double**:
`P = binexp(1+r, n)` (LSB-first square-and-multiply), `q = (P-1)/r`,
`tf = 1 + r·type`, `fv = -(pv·P + pmt·(tf·q))`, `pv = -(fv + pmt·(tf·q))/P`.
So Excel's forward annuity factor is PINNED bit-exact.

PMT reuses none of it. Metamorphic harvest (`gen_pmt_meta.py` → 621 FV probes,
`answers-pmt-meta-fv.json`): `P = -FV(r,n,0,1,0)` and `tf·q = -FV(r,n,1,0,ty)`
give Excel's OWN internal factors. Feeding them into `-(pv·P+fv)/(tf·q)`
(`pmt_meta_test.py`) scores **242/923 and is 0/109 on every small/tiny/negative
rate**. If PMT shared FV's forward factor this would close. It does not →
**PMT is a numerically-STABLE (discount) form; FV/PV are the naive forward form.
The siblings do not share the annuity factor.** (Human-written code reused the
helper for FV/PV but PMT's author chose a cancellation-safe path.)

## Finding 2 — the residual is the transcendental primitive, nothing else

Discount identity: `em = expm1(-n·log1p r)`, `v = 1+em = (1+r)^-n`,
`pmt = (pv + fv·v)·r / (tf·em)`.

Held-out ceilings (ranked by held-out, overfit-guarded):
- `race_pmt_substrate` (SSE2 body, x87/CRT transcendentals): champion
  **482/875** at `L=log1pCR E=expm1_internal arr=num/den·r`. Prior forward-pow
  zoo (`fit_pmt_stores`) ceiling was ~57% — same ballpark, different family.
- `race_pmt_x87stable` (WHOLE body per-op x87 double-rounded + x87 log1p/expm1):
  **460/875**, and **completely invariant to the 8-bit store-mask** (every mask
  ties). So body precision (SSE2 ≈ x87-DR) and spill-staging are NOT the gap.
- `pmt_combine_search` (plain-double forward final-combine, 23 arrangements):
  ≤262/875, small-rate-catastrophic — forward is wrong for PMT (confirms F1).

**n=1 isolation lane** (125 rows, pure `expm1(-log1p r)` test): hard ceiling
**62-65/125** identical across the plain closed form `-(pv·(1+r)+fv)/tf`, every
discount provider, forward and x87-DR. The misses **sign-flip with rate
magnitude** (Excel more-negative than the naive form at small rate, less-negative
above ~0.8%). That sawtooth = the exact rounding point of Excel's `log1p`/`expm1`,
which is **none of**: portable-CR `log1p`/`expm1`, the identified internal
Kahan-corrected F2XM1 `expm1_internal`, the raw base-2 hardware `fyl2xp1`/`f2xm1`,
or `ln(1+r)` (forming 1+r first). Ruled out by elimination: form, body precision,
store-mask, and all four known primitives.

## Status + NEXT PROBE (banked)

PMT = stable discount form; residual localized to Excel's **exact annuity
`log1p`/`expm1`** (a bespoke or CRT routine we have not reproduced). This is a
primitive-ID problem of the same class as the G3 internal-exp/expm1 lanes
(task #16, agent-solved). NEXT: isolate Excel's `em` bit-exactly via the
fv=0/ty=0 rows (single division `pmt = pv·r/(tf·em)` → em recoverable to ~1 ULP
by the exact-interval instrument, cf. b34), tabulate em(r,n) vs candidate
routines, and micro-stage search {raw-F2XM1-no-Kahan, RZ vs RN final store,
alt reduction, MSVC/Cephes expm1 forms} at 250-bit reference. CUMPRINC/PPMT/IPMT
(G6-07) inherit PMT's residual and close with it. Corpora ready:
`answers-pmt-heldout.json`, `answers-pmt-meta-fv.json`.

## Lane D continued — em-isolation capture (2026-07-21, Fable-designed probe)

Fable consult reframe: the PMT residual has TWO sources — (a) the small-rate
one-signed lower branch = the em primitive (a fixed-sign absolute error amplified
by 1/|em|), (b) the +branch = body/arrangement. Decisive probe (`gen_pmt_em_probe.py`
→ 13,752 live rows `answers-pmt-em.json`): **fv=0, type=0, pv∈{1,1.5}** collapses
the arrangement to `pmt = RN(pv·r/em)`, so `fl(pv·r/em_candidate)==pmt_excel`
directly scores each em routine. r log-spaced [1e-6,0.05] sign-mirrored ×
n∈{1..480 mixed-popcount}. **This grid IS Excel's em oracle** (recover em = r/pmt).

Racer `race_pmt_em.rs` (REAL x87 F2XM1/FYL2XP1, mpmath can't emulate the
instruction chain). Scores on the pv=1 collapsed grid (6876 rows):
- **internal-Kahan expm1 (on log1p-CR): 4050/6876 = 59% — BEST**, and UNIFORM
  across every |t|=|n·log1p r| regime (59% at |t|<0.25, 0.25-1, 1-4, 4+).
- CR expm1 48%; raw F2XM1-fold RN 48%, RZ/chop 37%; exp(t)-1 12%; no-fold 12%.
- Pure x87 SPILL (em EXTENDED, single final store, no double-store of em): 45% —
  WORSE than storing em to double first. So em IS materialized to double before
  the divide; the body is not a single-store extended spill.
- `v = pow_chain(1+r,-n)` (forming 1+r, Excel's POWER pow): **refuted, <1%
  everywhere** — the annuity does NOT form 1+r; it uses a genuine log1p.
- Regime-split (expfold small-|t| / powchain large-|t|): max 792/6876 — worse
  than uniform internal. NOT regime-split.

**Localization (final for this cycle):** PMT = stable discount form, x87
substrate, em = internal-Kahan-style F2XM1 expm1 on a natural log1p; the residual
is a UNIFORM ~1 ULP difference between `excel_expm1_internal` and Excel's exact
annuity expm1 on ~41% of the isolated grid — a sub-op rounding in the shared chain,
not a wrong family/regime/form. RULED OUT this cycle: forward decomposition,
Gnumeric forward-stable, body precision (SSE2≈x87-DR), store-mask, extended-fold
spill, chop store, exp-1, pow_chain(1+r,-n), ln(1+r), regime-split. **NEXT** (clean
handoff): micro-stage which sub-op of the internal-Kahan chain (the fFEXP final
store RN vs the Kahan `(u-1)·t/ln u` correction ops, or the log1p delivery) rounds
differently, scored against the 13,752-row em oracle; recover em=r/pmt to bits via
the exact-interval instrument and fit the per-op rounding. CUMPRINC/PPMT/IPMT
inherit + close with it.

---

# Lane E — RATE (G6-05), 2026-07-21 (agent-R)

RATE solver identified via the metamorphic lever (RATE finds r where FV(r,…)=fv;
FV is the closed forward-binexp balance). SETTLED: **forward-difference Newton in
r-space** (IRR's v-space sibling), FD step h=1e-6·x, stop |f|<1e-7 publishing the
stepped iterate, cap ~100, #NUM! on cap/domain/non-finite. Balance = pv·(1+r)^nper
+ pmt·(1/r+type)·((1+r)^nper−1) + fv. **POWER = x87 87tran exp·ln** (confirmed by
#NUM! basin: x87chain 15/15 vs binexp/powf 10/15). **Basin 116/116** all corpora.
Secant refuted (false-converges on #NUM! rows). OPEN: exact bits 0-2/101 — the
balance catastrophic-cancellation op-graph (~1 ULP-of-f amplified 5-60× near root),
not closed by {dbl, Ext80, per-op-DR}×{5 pow}×{4 deriv}×{2 arr}. Racer race_rate.rs.
Next lever: r1/r2 near-root one-step ladder (single Newton step, no trajectory
chaos) to pin the balance spill + FD-h form.

# Lane D — PMT combine (G6-01), 2026-07-21 update (coordinator + agent-Q)

The combine (given em) is NOT a single-shared-quantity form: control-clean tests
(agent-Q) show single-em all-8-pv REAL 7.1% vs mismatched-CONTROL 0.0% (genuine but
only 7%); forward-(P,q) "82%" was pure over-fit (control 80%). Coordinator's 256-
CONSECUTIVE-pv sweep (answers-pmt-combsweep.json, over-fit-proof) independently
refutes every 1-/2-constant form (shared-em ≤214/256, forward-(P,q) no fit even
P±500ulp, fused/recip/x87-div all ≤205/256). ROBUST facts: pmt(pv)/pmt(1) within ≤1
ulp of pv (pv scales a base); the residual vs RN(pv·base) is ONE-SIDED (Excel
systematically MORE negative: {0:112,+1:126,+2:13} at (0.05,12)) → an extended
accumulator / truncation biasing high; pv·r is NOT pre-rounded (exact-num divide 62%
> pre-rounded 55.6%). CONCLUSION: the combine carries a SECOND independently-rounded
(r,n)-quantity (the forward P,q pair or v alongside em), with an x87 extended
intermediate. Path: pin the 2nd quantity (v) model-free from the fv≠0 rows
(answers-pmt-fvty.json) + gold em, over-fit-controlled; validate the final op-graph
on the 256-consecutive-pv sweep. Fable consult running on the exact x87 spill.

## Lane D — PMT COMBINE SOLVED (2026-07-21, Fable consult): quotient-first H-DF

BREAKTHROUGH. Every combine form the coordinator + agent-Q raced multiplied
`pv·r` FIRST and capped ~55-80% on the over-fit-proof 256-consecutive-pv sweep.
Fable's insight: the VB/BASIC financial lineage does **quotient FIRST, `·rate`
LAST**. The combine is:
  **pmt = RN( RN( num / den ) · r )**,  num = pv + fv·(1+em),  den = em·tf,
  tf = 1 + r·type.   (fv=0,type=0 → RN(RN(pv/em)·r).)
Fable PROVED product-first impossible via an anchored-phase argument: pv=1.0 is
exact so RN(pv·r)=r forces the product stage to phase 0 → a slope-1.6 staircase
{0,2,3,5,6,8,10}, which no divisor (any precision) can reshape into the observed
{0,1,3,4,6,9,11}; the 3-step jump alone requires TWO coarse pv-dependent stages,
which a single product/divide cannot produce. (This impossibility argument is
Last Bit material.)

VALIDATION (`race_pmt_hdf.rs`, real x87 internal-Kahan em):
- Consecutive-pv sweep: H-DF **256/256 on ALL 9 sweeps** (product-first 134-214);
  combsweep corpus **2304/2304 = 100% EXACT** with the COMPUTED (not searched) em.
- Full held-out 482/875 exact / 88% ±1; em corpus 10801/13752 (78%/92% ±1);
  pvladder 43026/55008 (78%/92% ±1). fvty 42%/74% (fv≠0 wants a v-source check:
  v=1+em vs v=exp(tau)).
So the COMBINE ARRANGEMENT IS SOLVED; the entire remaining ±1 ULP residual is `em`
bit-exact (agent-P's x87 expm1 lane) — NOT a combine gap. The prior gold em oracle
was product-first-contaminated; re-extract em under H-DF (256-pv sweep → unique em
per (r,n)) for a clean agent-P oracle. Next: Fable's r=2⁻⁵ probe (exact ·r) to pin
em to ~2⁻⁶⁰ and settle the divide spill (em f64 vs extended).

### H-DF em oracle (r=2⁻ᵏ trick, 2026-07-21)
Fable's power-of-2-rate probe generalized: at r=2⁻ᵏ, `·r` is exact → H-DF collapses
to a pure divide → em pinned to <0.01 ulp by 256 consecutive pv. Captured a broad
grid (6 r × 9 n, batch-pmt-po2.json) → **Excel's EXACT em at 46 (r,n)**
(pmt_em_hdf_oracle.json). Result: **35/46 match correctly-rounded expm1, 11/46 are
±1 ulp off** (8 at +1, 3 at −1). That is the ENTIRE remaining fv=0 residual, pinned
to the bit and decoupled from the combine. race_pmt_hdf (internal-Kahan em):
combsweep 2304/2304 (100%), po2 11990/13824 (87%), r25 1539/2304 (67%) — internal-
Kahan ≈ CR, so it misses exactly the 11 off-CR (r,n). CLOSURE = (a) the exact expm1
op-graph matching all 46 (agent-P), and (b) the fv≠0/ty=1 H-DF num/tf details
(agent-Q; fv=0/ty=0 skeleton solved). agent-Q's earlier "single-divide empty" was
for PRODUCT-first RN(NUM/em) — H-DF is QUOTIENT-first (two roundings), which its
"multi-rounding" instinct correctly anticipated.

### PMT closure state (2026-07-21, agent-P + agent-Q on H-DF)
- **expm1 SOLVED (agent-P, 87/87 bit-exact)**: em = internal double-rounded Kahan
  `(u−1)·t/ln(u)` for |tau|<1, `exp(tau)−1` for |tau|≥1; u=exp(tau), reproduces ALL
  46 HDF + 41 pox oracle points PROVIDED log1p is Excel's actual value. The exp/ln
  primitives are proven exact (worksheet EXP(t)==u, LN(u)==CR, all 12 probe args).
- **tf placement PINNED (agent-Q, 256/256)**: pmt = RN(RN(RN(num/em)/tf)·r),
  tf=RN(1+r·type) SSE2 — tf is a SEPARATE middle divide between /em and ·r (den=em·tf
  and tf-last both 0/256). num=pv+fv·v. type=0 → tf=1 → reduces to H-DF.
- **RESIDUAL = Excel's non-CR log1p** (the sole fv=0 unknown): a genuine Excel
  imprecision (per "Excel imprecision is still a bug", reproduce not fix). Standard
  log1p (fyl2xp1/portable/ln(1+r)/fdlibm) are ALL bit-identical to CR at these rates.
  Coordinator n=1 map (answers-pmt-log1p.json, 113 r × 256 pv, tau=−log1p r isolates
  it): deviation is a STRUCTURED ±1-2 ulp non-CR pattern concentrated near 2⁻⁴/2⁻⁵
  (agent-P's pox map: uniform +1 at 2⁻⁵,2⁻⁴; n=1 map shows ±1-2 across their
  neighbors, 2⁻⁶→−1, 2⁻²→−1). Same log1p feeds agent-Q's v=(1+r)^−n, so IDing it
  closes both. Open: (a) the exact log1p op-graph (agent-P, n=1 oracle captured);
  (b) the fv num=pv+fv·v op-order (agent-Q, fv=±1 non-degenerate sweep captured).
So PMT is at NEAR-TOTAL closure: combine + expm1 solved bit-exact; only a non-CR
log1p imprecision and the fv-num assembly remain.

### PMT COMBINE OP-GRAPH — FULLY PINNED (agent-Q, 2026-07-21, over-fit-safe)
From the non-degenerate fv=±1 consecutive-pv sweeps, the complete final combine
(all SSE2 double, quotient-first):
```
  num = RN(pv + fv·v)        # v = (1+r)^-n discount factor; fv·v then +pv
  q1  = RN(num / em)         # em = (1+r)^-n − 1
  q2  = RN(q1 / tf)          # tf = RN(1 + r·type); type=0 → tf=1 → q2=q1
  pmt = RN(q2 · r)           # ×rate LAST
```
Discriminated 256/256: num=pv+fv·v (not two-term, not x87-extended — inverting gives
num−pv = v = constant across pv); tf is a SEPARATE MIDDLE DIVIDE (den=em·tf → 0/256,
tf-last → 0/256, /tf-middle → 256/256); fv=−1 v-insensitive 256/256; fv=0 → H-DF
99.7%/0%-control. The whole-skeleton residual (49.9%, bounded ±3, +biased) is ENTIRELY
the coupled {em, v} precision — em and v cannot be separated (no single double-v closes
fv=+1), because both flow from the SAME internal tau=−n·(non-CR log1p).

**PMT is therefore reduced to a SINGLE open primitive: Excel's non-CR log1p.** Combine
(agent-Q) + expm1/exp arithmetic (agent-P, 87/87) are both solved bit-exact. Full PMT
= the op-graph above + {em=expm1(tau), v=exp(tau)} once Excel's exact log1p is IDed
(agent-P's final lane; n=1 oracle answers-pmt-log1p.json captured).

### log1p — the final open primitive (2026-07-21; 3rd Fable consult REFUTED end-to-end)
Fable proposed Excel's log1p = the **Kahan companion trick** `u=fl(1+r); ln(u)·r/(u−1)`
(the algebraic dual of the solved expm1), with a compelling period-law argument: ε=u−(1+r)
is a sawtooth of period 2⁻ᵉ per binade, matching the dense-sweep ramp-at-2⁻⁸ (period 256)
and ripple-at-2⁻³ (period 8). BUT end-to-end race (race_pmt_hdf, all op-orders + extended
+ x87-ln) REFUTES it: every variant makes combsweep 2304→1724 and helps nothing. Diagnosis:
the po2 rates are all **ε=0** (1+2⁻ᵏ exact → Kahan correction r/(u−1)=1 → degenerates to plain
ln(u)), so they can't discriminate; the ε≠0 combsweep rates DO, and there **Excel matches CR
log1p, not the Kahan form**. So Excel's PMT log1p is CR on well-conditioned (ε≠0) rows and
non-CR only on a specific subset — NOT the Kahan companion, NOT any standard routine. RULED
OUT now: CR/portable, fyl2xp1 (all deliveries), fdlibm, Cephes, ln(1+r)/fyl2x, Kahan
companion. STATUS: the sole open PMT primitive; a genuine Excel imprecision, characterized
(faithful ~0.6 ulp, non-CR, dev-sign follows sub-ulp position, smooth per-binade error curve
of period 2⁻ᵉ), fingerprint data captured (answers-pmt-log1p + answers-pmt-denselog1p, 3
binades × 256 consecutive r). NEXT-SESSION: fit the routine from the dense curve (Fable probe
A: dev-vs-low-bits phase-lock + ε=0 sublattice; probe C: negative-r/binade-2⁻¹ period tests).
**PMT is otherwise fully solved: combine (H-DF, quotient-first, tf middle divide) + expm1
(internal Kahan) are bit-exact; only this one non-CR log1p imprecision blocks a bit-exact
landing.**

### log1p — the "non-CR log1p" is a MISDIAGNOSIS; the wall is expm1 double-rounding (2026-07-23)
The prior section's premise is WRONG and is retracted here. Excel's PMT log1p is
**CORRECTLY ROUNDED**, and the residual attributed to it is actually the expm1/tau
double-rounding. Decisive evidence, all model-free:

1. **LN at exactly-representable 1+r = CR, 148/148.** At r=2⁻ᵏ (and r=j·2⁻⁸,j·2⁻⁹) the
   argument 1+r is EXACT, so log1p(r)=ln(1+r) with no argument rounding. Direct live
   `LN(1+r)` oracle (batch-ln-exact, 148 pts spanning the dense-sweep region): **0 non-CR**.
   The x87 `FYL2XP1`/`FYL2X`-on-exact-ext hardware (real inline asm on this AMD host) also
   equals CR there — so log1p is not the deviation source.
2. **Internal exp is bit-exact.** For all 234 |tau|<1 po2×n points, live `EXP(tau_d)` == the
   x87 `excel_exp` emulation, **234/234** (batch-em-exp). `LN(u)` likewise matches.
3. **The residual is the expm1 |tau|<1 branch.** Model-free em oracle (r=2⁻ᵏ trick × n∈
   {1..64}, answers-pmt-po2n, 258 pinned (r,n)): the all-double Kahan `(u−1)·t/ln(u)`
   reproduces **163/234 (70%)** on |tau|<1; the |tau|≥1 (`u−1`) branch is **100%** (all
   3840 pts). With tau, u=exp(tau), and ln(u) ALL proven-identical doubles to Excel's, no
   double-op SEQUENCE tested closes the gap: 12 forms raced (prod-first / Kahan-canonical /
   div-first associations; additive corrections `b+b·(t−lnu)/lnu` and relatives; `t·b/lnu`
   numerator; denominators `fyl2x(u)`/`fyl2xp1(u−1)`/`log1pCR(u−1)`) — ceiling **163**,
   second cluster 145. Extended stagings (ext tau, ext correction, full-ext, ext-divide)
   and the base-2 `F2XM1(−n·log2(1+r))` path are all WORSE (99–152). So Excel's em on the
   71 miss points ≠ any Kahan/expm1 op-graph over the observable {tau,u,ln u}.

**Reconciliation with the "expm1 SOLVED 87/87":** the 87 HDF+pox points did not stress the
|tau|<1 double-rounding (mostly |tau|≥1 or a favorable subset). The po2×n oracle is the
held-out that exposes the true 70% ceiling — a textbook [[validate-workflow-ids-on-heldout]]
correction. **PMT residual is therefore an expm1 |tau|<1 double-rounding OP-GRAPH WALL**
(class of [[remaining-lanes-are-opgraph-walls]]), NOT a log1p imprecision. The large-|fv|
assembly failures (fvsweep 0/1024 under discount `(num/em)/tf·r`; product-order denom
`(num·r)/(tf·em)` 512/1024) are the SAME wall amplified: v=(1+r)⁻ⁿ=1+em cancels for large n
(v tiny) and, even with v=exp(tau), the em denominator carries the ±1. Discount combine
`[0] (num/em)/tf·r` remains Excel's form for fv=0 (combsweep 2304/2304, pvladder best);
forward-exp `−(pv·P+fv)/((P−1)/r)/tf` with x87 P=exp(n·log1p r) is worse on every corpus.
Tooling: race_log1p{,_e2e,_off}, race_em_staging{,2}, race_expm1_{small,denom,mixed,addcorr},
diag_fv{,2}, diag_fwd; oracles answers-{ln-exact,pmt-po2n,em-exp,em-ln}.json.

### PMT em is NOT Excel's standard expm1; the wall is REAL, toward-zero-biased (2026-07-23, big workflow)
A 12-agent exploration workflow + coordinator oracle work resolved WHAT the residual is and
exhaustively bounded it. Three decisive new results:

1. **PMT's em ≠ Excel's standard expm1.** `EXPON.DIST(x,1,TRUE)=1−e^−x` exposes Excel's expm1
   DIRECTLY: `expm1(tau) = −EXPON.DIST(−tau,1,TRUE)`. Excel's EXPON.DIST expm1 == the all-double
   Kahan model **232/234**, but PMT's pinned em matches that same Kahan only **165/234** — and at
   IDENTICAL tau (n=power-of-two → tau exact) EXPON.DIST gives Kahan while PMT gives something
   else. So PMT's annuity `(1+r)⁻ⁿ−1` is a **financial-body-specific routine, distinct from the
   statistical expm1** (which the old "87/87" measured). This is why no {tau,u,ln u} op-graph closes it.
2. **The residual is REAL, not a po2 (r=2⁻ᵏ) sampling artifact.** On generic rates `r=m·2⁻ᵏ`
   (m∈{3,5,7} odd, 1+r still exact → log1p CR), the all-double Kahan still matches only **61/90 (68%)**
   with the SAME structure: signed residual `em_pinned−Kahan = {0:61,+1:25,+2:3,+3:1}`, **never
   negative** — a systematic **toward-zero bias** (Excel underestimates |expm1|), pure `{0,+1}` at
   small |tau|. Consolidated 324-point `delta(tau)=em_pinned−CR_expm1` is a **±1–2 ULP spread with a
   toward-zero bias, NOT a smooth curve** → a genuine last-bit op-graph effect, not a fittable
   coefficient error.
3. **Exhaustively refuted (multi-agent SLP enumeration + coordinator x87 races):** extended-x87
   single-store (F2XM1-native 106, ext-u−1 99, ext-Kahan 133, all < 163), polynomial/rational
   (fdlibm 129, Cephes 84, CR-expm1 133 — Excel is LESS accurate than CR, so not a library expm1),
   directed rounding / chop of Kahan (112–119), binexp power (refuted on |tau|≥1: 18/24 vs exp 100%).
   The all-double Kahan `(u−1)·t/ln(u)` is the firm **163/234 ceiling**; a double-rounded numerator
   `RN53(RN64(b·t))/ln(u)` nudges to 165. **Interpretation: a hand-coded inline expm1 (tiny-arg fast
   path that overshoots toward zero + a reduced main path) that systematically underestimates |expm1|
   by ≤1 ULP — a real Excel imprecision, op-graph outside every tested family.** Reproduce, don't fix.

**Provenance (workflow, verbatim public source):** LibreOffice/OpenOffice `ScGetPMT` and Gnumeric
`pow1pm1` confirm the EXPRESSION `em=expm1(±n·log1p r)` but use POSITIVE-tau forward assembly +
a library (near-CR) expm1 — refuted as Excel's op-graph (Excel is −tau discount + non-CR). numpy/
VB6/.NET use `pow(1+r,+n)` subtractive — refuted. **No open reference implementation matches Excel's
−tau discount + bespoke non-CR expm1 arrangement; Excel PMT is a distinct, older, x87-native MS routine.**

**Related-function inheritance map (workflow):** PMT → {IPMT, PPMT} → {CUMIPMT, CUMPRINC} (IPMT/PPMT
consume PMT's payment; CUM* sum them). FV/PV (forward binexp, closed 149/149 + 48/48), NPER (x87,
closed 1729/1729), NPV, RATE (FD-Newton, mechanism IDed), IRR do NOT inherit PMT's expm1. So closing
PMT's expm1 op-graph closes five functions. NOTE: the naive `IPMT(per)==RN(FV(per−1)·r)` inheritance
was REFUTED against the live oracle (0/9, diverging) — the exact IPMT balance recurrence needs its own
identification, not the simple FV·r form. fvsweep is a DEGENERATE corpus (Excel returned constant across
256 fine-sweep pv — a generation artifact); drop it as a combine oracle.

Tooling added: race_ext_em, race_genrate, export_em, diag_fwd; direct-expm1 oracle answers-expondist.json;
generic-rate em answers-pmt-genrate.json; POWER=binexp confirmation answers-pow-{po2neg,po2pos,genneg}.json;
consolidated em_consolidated.csv; fast Python op-graph tester work/.../expm1_optest.py; full agent digest
work/.../WORKFLOW_RESULTS.md + COORDINATOR_NOTES.md.

### SLP/DAG enumeration EXECUTED — confirms the wall, does not break it (2026-07-23)
Per user direction, mounted the systematic straight-line-program search on the |tau|<1 em. Since u=exp(tau)
and lnu=ln(u) are captured EXACT doubles, ran the enumeration in pure Python (float=RN53) for instant
iteration, plus x87 stagings in Rust. Exhaustive result — NOTHING exceeds the 163 (165 w/ x87-spill num)
ceiling:
- **Op-graph enumeration over {tau,u,lnu,b=u-1,consts}** (Kahan associations, Newton subtractive
  corrections `b−u·(lnu−t)` / `b−b·(lnu−t)/lnu` = 144-145, div-first/mult-first, reciprocal): champion is
  `(u−1)·t/lnu` = **163/234**; independently corroborates agent-M's 128-mask enumeration.
- **Truncated-Taylor / series fast-path** (T2..T5, Horner): all WORSE than Kahan in every |tau| regime
  (best T5=65 on tiny-tau vs Kahan 77). Not a polynomial fast path.
- **x87 per-op double-rounding (spill)** (num/div/tau each RN64→RN53, matching the XNPV spill-loop
  precedent): num-double-rounded = **165/234** (+2), no help on generic (61/90). Not the mechanism.
- **Extended tau → double u** (u=RN53(exp(tau_ext)) from extended log1p, testing 1-ULP boundary shifts of
  u): fixes 0-1, breaks 1-8 — u is robust to the argument's extended tail. Refuted.
- **delta(tau)=em_pinned−CR_expm1 is a NOISY ±1-2 ULP lattice** (roughness ~0.6, sign flips between
  adjacent tau — NOT a smooth monotonic curve). This RULES OUT minimax-rational coefficient recovery (a
  rational's error-vs-CR is smooth). So the residual is a genuine last-bit op-graph effect, not a fittable
  coefficient error.
**Verdict (SUPERSEDED below):** the PMT expm1 |tau|<1 residual is an IRREDUCIBLE ≤1 ULP op-graph wall — Excel's bespoke inline
routine produces a toward-zero-biased ±1 ULP scatter not determined by {tau, exp(tau), ln(u)} or their
extended forms, and not by any polynomial/rational. Tooling: race_x87spill_em, race_tauext_u.

### BREAKTHROUGH — em is NOT a function of tau_double; the argument is EXTENDED (2026-07-23, continued push)
The "irreducible wall" verdict above is SUPERSEDED. A designed **tau_double-collision experiment** cracked the
reason every double op-graph caps at 163: **the argument carries sub-double-ULP information.**
- **Design:** for 7 target tau₀ (doubles in [−0.7,−0.02]), find ~18 (r,n) each with `RN(−n·log1p_CR(r))=tau₀`
  (same double tau) but different exact `−n·ln(1+r)`. Capture PMT (128 consecutive pv each, 16384 probes);
  pin em per config (answers-pmt-collide.json). **em VARIES 1–3 ULP within every group** (pure function of
  tau_double would give ONE em/group).
- **Doubt-probed hard and it HELD:** (a) all 116 pins are UNIQUE (0 ambiguous) — not a pinning artifact;
  (b) the combine is **confirmed SSE2** `RN(RN(pv/em)·r)` — the x87-double-rounded and quotient-extended
  combines reproduce ZERO configs, so the variation is NOT a general-rate combine artifact; under the correct
  SSE2 combine, 7/8 groups still need multiple em.
- **Interpretation:** Excel's financial expm1 keeps `tau` (= −n·log1p(r)) in an **80-bit x87 register, never
  spilled to a 53-bit double**, so em depends on tau's bits 54–64. This is exactly why {tau_double, exp, ln}
  op-graphs cap at 163 — they can't see the extended tail. em weakly tracks exact_tau (corr 0.24) but is
  NON-monotonic in it, and idealized round53(CR64(expm1(round64(exact_tau)))) scores only 72/116 (WORSE than
  53-bit) — so the extended dependence is via Excel's SPECIFIC x87 op-graph (fFEXP/FYL2XP1 with their
  ~1-ext-ULP microcode error, which is r-dependent), NOT idealized round-to-64. My fyl2x/fyl2xp1-based extended
  models get 83/116 (right structure, wrong tail) — the exact internal **log1p delivery + `×n` staging** is the
  remaining unknown. NOTE: "log1p is CR" was proven only for WORKSHEET LN (spilled to double); the financial
  body's internal log1p is evidently kept extended and its 64-bit tail is what matters.
- **This REFRAMES the search from the expm1 correction to the EXTENDED TAU FORMATION**, and gives a sharp
  discriminating oracle (the collision set: 7/8 groups need the exact extended op-graph, not just the plurality).
  Tooling: race_spill_exhaustive (spill×PC×RC×ln-delivery×assoc, single-instruction transcendentals),
  race_collide_search, doubt_combine. Oracle: answers-pmt-collide.json + collide-meta.json.

### CORRECTION — the collision variation is DOUBLE-level faithful-not-CR log1p, NOT extended argument (2026-07-23)
The "extended argument" interpretation above is RETRACTED (a doubt-probe caught it; combine is still confirmed SSE2).
Decisive checks: (1) The collision-inversion agent found `CR-expm1(exact_tau)` scores 72/116 — WORSE than
`CR-expm1(tau_double)` at 82 — so em does NOT track the extended (exact) tau; and all accurate 64-bit log1p routines
(CR/FYL2XP1/fdlibm) are indistinguishable at this oracle (within 2 ext-ULP vs a ~1000-ULP acceptance band). (2) The
collision design shares `tau_double` ONLY under mpmath-CR log1p (1 distinct/group); under **C-library `math.log1p` the
configs have 3–4 distinct `tau_double`/group** — matching em's 2–4 distinct values. So **Excel's internal log1p,
spilled to a double, is a FAITHFUL ~1-ULP routine, NOT correctly-rounded** (close to C-lib `log1p`), and my configs that
"share tau0" under CR log1p actually have DIFFERENT Excel-`tau_double`. em IS `g(tau_double)` after all — I'd computed
`tau0` with a too-perfect (CR) log1p. Grouping em by C-lib-`tau_double` cuts the conflicts (7/7 CR-groups → 12/20
C-lib-groups multi-em) but isn't clean, so the exact faithful log1p isn't C-lib either — it's a specific ~1-ULP routine
(FYL2XP1-class) to be pinned. **"log1p is CR" holds ONLY at exact-1+r (po2, worksheet LN 148/148); at general r the
financial-body log1p is faithful-not-CR, and that is a large chunk of the general-rate PMT residual (heldout).**

**Corrected two-component picture of the PMT residual:**
1. **General-rate log1p-not-CR** (the collision variation, and most of the heldout ±1 ULP): tau_double = RN(−n·log1p_EXCEL(r))
   where log1p_EXCEL is a faithful ~1-ULP routine (FYL2XP1/C-lib-class), not CR. IDing it fixes the general-rate residual.
   Invisible at po2 (exact-1+r, where all faithful log1p = CR).
2. **po2 expm1 op-graph wall** (71/234, confound-free — log1p=CR there): the all-double Kahan `(u−1)·t/ln(u)` ceilings at
   163/234 over {tau,u,ln u}; a separate, smaller residual (the genuine expm1 combine rounding).
NEXT: pin log1p_EXCEL by the "em is a clean function of tau_candidate" test across {FYL2XP1-hw→double, C-lib, fdlibm,
MS-CRT} on the collision + genrate oracles; then re-attack the po2 expm1 wall separately.
