# PMT & the Annuity Cluster — Historical Takeover Brief

**Status date:** 2026-07-25 · **Lane:** W109 G6-01 (+ G6-07) · **Audience:** whoever picks up the PMT
identification next, with no prior context.

> **Current-authority warning (2026-08-09):** this brief is historical and its
> “structurally identified”, single-residual, sibling-inheritance, and search
> boundary language is not current campaign truth. The July “irreducible / needs
> provenance” conclusion was retracted. Fresh current-build work refutes tested
> low-word/smooth corrections, proves only a local `832/832` power-of-two timing
> identity, and leaves the frozen general-rate tail non-exact at best `378/480`.
> Read
> [`W109_PMT_INTERMEDIATE_AND_TIMING_DISCRIMINATION_20260809.md`](W109_PMT_INTERMEDIATE_AND_TIMING_DISCRIMINATION_20260809.md)
> and the current G6-01 catalog row first. G6-01 remains open and actionable.

Read this first. It supersedes the narrower `W109_G6_PMT_RESUME_20260723.md` (still accurate but pre-dates
the enumerator campaign). The field-diary companion with the narrative is `docs/notes/PMT_EXPM1_IDENTIFICATION_STORY.md`.
The canonical open-discrepancy tracker is `docs/OXFUNC_EXCEL_DISCREPANCY_CATALOG.md`, row **G6-01**.

---

## 0. One-paragraph summary

Excel's `PMT` and its four inheritors are structurally identified and their production implementation was
corrected and landed. What remains open is a **single last-bit residual inside one private internal routine**:
the discount term `em = (1+r)^-n − 1`. On a 234-row model-free oracle, the best clean-room model reproduces
**165/234** exactly; the other 69–71 rows sit exactly one ULP away with a systematic toward-zero bias. Six
independent attack modes — including an actual exhaustive op-tree enumerator — have failed to close it. The
open question is *not* recognition (we would know the answer instantly if we saw it) but **search and
observability**: every operand the routine consumes is pinned, yet no reachable program over those operands
produces Excel's bits.

---

## PART I — CONTEXT

### 1. What OxFunc is

OxFunc is a Rust reimplementation of Excel's worksheet function library whose acceptance criterion is
**bit-exact agreement with live Excel**, not mathematical correctness. Every function must return the identical
IEEE-754 `binary64` bit pattern that Excel returns for the same inputs — including where Excel is *less*
accurate than the true mathematical result.

Two standing rules follow, and they are absolute:

- **Never accept a divergence.** Any OxFunc↔Excel mismatch is a defect, including on degenerate or absurd
  inputs. "Won't fix" and "acceptable difference" are not available. The task is always to reverse-engineer
  Excel's exact deterministic rule.
- **Excel's imprecision is still a bug — ours.** If Excel is 1 ULP off the correctly-rounded answer and OxFunc
  is exact, OxFunc is wrong. Repair direction is always *toward Excel*, never toward analytic correctness.

The public sub-project *The Handbook of Excel Functions* (github.com/DnaCalc/ExcelFunctionsHandbook) publishes
findings from this work, which is why the clean-room posture below is load-bearing rather than decorative.

### 2. The clean-room principle — ABSOLUTE, NON-NEGOTIABLE

**We never disassemble, decompile, debug, or otherwise inspect Excel or any Microsoft binary. We never propose
it. We never accept a result derived from it.** This is a standing policy, not a preference, and it is not
subject to cost/benefit argument at any point in the search.

Permitted evidence sources, exhaustively:

1. **Behavioral oracle.** Drive live Excel with inputs, read outputs. Arbitrary volume. This is the primary
   instrument.
2. **Public sources.** Published algorithm literature (Cody & Waite, Goldberg, Kahan, Muller), public-domain or
   permissively-licensed reference implementations *read for their mathematics*, vendor documentation, Intel
   architecture manuals (x87 instruction semantics), and third-party reverse-engineering write-ups published by
   others (e.g. Morten Welinder's Gnumeric blog).
3. **The host CPU.** Executing real x87 instructions (`F2XM1`, `FYL2X`, `FYL2XP1`, `FSCALE`, `FRNDINT`) on this
   machine to observe hardware rounding curves is measurement of *our own hardware*, not of Excel.
4. **Public C API probing** of DLLs through documented, exported entry points is acceptable; reading their code
   is not.

**Licensing constraint on top of clean-room:** OxFunc is MIT-licensed. We therefore may not copy code from
GPL/LGPL sources (Gnumeric, LibreOffice) or from restrictively-licensed references. We may read such sources to
learn *what algorithm* is used and then implement independently, and we may cite them as evidence about
Excel's behavior. Public-domain sources (fdlibm/SunPro) and published book algorithms are safe to implement
from directly. When in doubt, derive the mathematics from first principles and validate against our own oracle.

**Practical consequence for this lane:** clean-room forbids *reading* the code. It does not forbid
*determining* what the code computes — that is the entire purpose of a behavioral oracle. Constants and
coefficients that exist nowhere but inside a binary are still fully observable through their effect on output
bits, and a 234-row exact-bit oracle over-determines any small coefficient set by two orders of magnitude.
Unknown coefficients are therefore a **search-and-constraint-solving problem**, never a stopping point; the
only question they raise is which mechanism recovers them most efficiently (see §21 item 3 for the exact
formulation). Nothing in the clean-room policy has blocked, or can block, this lane.

### 3. Excel's numeric substrate (established across the wider W109 campaign)

This model is well-validated and should be assumed by anyone working here:

| Layer | Substrate | Evidence |
|---|---|---|
| Worksheet operators (`+ − * /`), most modern function bodies | **Pure SSE2 `binary64`**, one rounding per op | broad |
| `EXP`, `LN`, `LOG10`, `LOG`, `POWER` | **Legacy x87 CRT chain** (87tran.asm lineage, control word `0x133F` = PC64/RN) | bit-exact reproduced via inline asm |
| Legacy *financial* function bodies | **x87, frequently a per-op double-rounded "spill loop"** — compute at PC64 in-register, `FSTP` to `double`, reload | proven for XNPV; strong prior elsewhere |
| Statistical distribution substrate | DCDFLIB `GRATIO`/`BRATIO` derivatives with **site-dependent publication** (RN wrapper at one call site, chop at another, extended delivery at a third) | G3-01 lane |

Two facts from that table matter enormously here:

- **The host is 64-bit Excel → MSVC x64 → the compiler cannot emit x87.** Any compiled body is SSE2. All
  extended-precision freedom therefore lives inside *hand-written assembly library routines* and, critically,
  in their **delivery convention** (what precision/rounding a transcendental result carries when its caller
  consumes it). This kills a large hypothesis space and should be internalized before designing experiments.
- **"Site-dependent publication" is real and precedented.** The same internal `exp` chain is published three
  different ways at three call sites in the distribution lane. So "PMT's `expm1` differs from `EXPON.DIST`'s
  `expm1`" is not an exotic hypothesis; it is the house pattern.

### 4. The x87 emulation layer

`crates/oxfunc_core/src/excel_numeric/x87.rs` (feature `research-x87`) provides real-hardware primitives via
inline asm, all control-word parameterized:

- `Ext80` — an opaque 80-bit value (`[u8; 10]`), `Copy`.
- `ext_add/sub/mul/div(a, b, cw)` — `FADD/FSUB/FMUL/FDIV` at the given CW.
- `ext_fyl2x(y, x, cw)` = `y·log2(x)`; `ext_fyl2xp1(y, x, cw)` = `y·log2(1+x)` (domain `|x| < 1−√2/2`).
- `ext_f2xm1(x, cw)` = `2^x − 1` (domain `|x| ≤ 1`); `ext_scale`, `ext_rndint`, `ext_sqrt`, `ext_sin/cos/tan`.
- `ext_from_f64` (exact widening), `ext_to_f64(x, cw)` (the **`FSTP` store barrier** — this is where
  double-rounding happens).
- Constants: `ext_ln2` (`FLDLN2`), `ext_l2e` (`FLDL2E`), `ext_one`; plus `FLDLG2` via one-line asm.
- Control words: `CW_PC64_RN = 0x133F`, `CW_PC53_RN = 0x123F`, `CW_PC24_RN = 0x103F`; OR `0x0C00` for
  round-toward-zero (chop), `0x0400`/`0x0800` for down/up.

**Critical modelling distinction, frequently gotten wrong:** an SSE2 op is `RN53(exact(a,b))` — a *single*
rounding of the exact result, which for a product means rounding the exact 106-bit product. An x87 PC64 op
followed by a store is `RN53(RN64(exact(a,b)))` — a *double* rounding. These are different functions and
differ on real inputs. The enumerator models both as distinct op families; any hand-written experiment must
too.

---

## PART II — THE PMT CLUSTER

### 5. The functions and their inheritance

```
PMT  ──► IPMT ──► PPMT ( = pmt − ipmt )
  │        └────► CUMIPMT
  └──────────────► CUMPRINC
```

`FV`, `PV`, `NPER`, `NPV`, `RATE`, `IRR` do **not** inherit — they use different internal kernels (see §7).
Closing PMT closes all five; nothing else in the financial family is blocked on it.

### 6. Production state (landed, in tree)

`crates/oxfunc_core/src/functions/financial_time_value_family.rs`

```rust
// pmt() — corrected op-graph, commit 1eb9011
let neg_log = -(periods * excel_log1p(periodic_rate));   // tau = −n·log1p(r), CR log1p
let em = excel_expm1_internal(neg_log);                  // (1+r)^−n − 1, x87 Kahan
if em == 0.0 { return Err(FinancialError::Num); }
let inv_factor = 1.0 + em;                               // v = (1+r)^−n
let tf = timing.factor(periodic_rate);                   // 1 + r·type
let numerator = present_value + future_value * inv_factor;
let result = ((numerator / em) / tf) * periodic_rate;    // SSE2, quotient-first, ·r LAST
```

Two landings this campaign:

- **`1eb9011`** — replaced a *refuted* reciprocal-multiply combine + portable `exp`/`expm1` substrate with the
  pinned quotient-first SSE2 combine and the x87 substrate. Live-Excel measurements:
  `heldout 46%→56%`, `combsweep 62%→100%`, `po2 61%→87%`, `genrate 47%→73%`, `fvty 36%→43%`,
  `fv1sweep 36%→50%`. 1513 lib tests green, zero regressions.
- **`5082589`** — IPMT epsilon-band bug: `if periodic_rate.abs() < EPSILON { return Ok(0.0) }` collapsed *tiny
  and negative* rates to zero and dropped the sign. Now exact `== 0.0`. Live Excel:
  `IPMT(1e-13,1,360,2e5) = −2e-8` must flow through the main path. Regression test
  `ipmt_tiny_rate_flows_through_main_path`.

Note the test asserts *behavior* (flows through, correct sign, magnitude within 1–2 ULP) not exact bits for
main-path values, because IPMT inherits PMT's open residual. Do not "fix" that test by pinning bits until the
residual closes.

### 7. Sibling kernels (established, useful as contrast)

| Function | Internal kernel for its `(1+r)^n`-type term | Evidence |
|---|---|---|
| **FV, PV** | naive **forward binexp** in plain SSE2 double: `P = binexp(1+r, n)`, `q = (P−1)/r` | var0 149/149 and 48/48 bit-exact |
| **EFFECT** | **integer binexp `pow` − 1** | 305/315 on a fresh grid |
| **RRI** | `pow(base, 1/n) − 1`, **plain subtract** (`exp(arg)−1` = 152/154) | fresh grid |
| **EXPON.DIST** | the **statistical** `expm1` — all-double Kahan, **232/234** | direct oracle |
| **PMT** | a **private** discount `expm1` — Kahan, only **165/234** | this lane |
| **RATE** | forward-difference Newton in r-space, x87 `POWER` chain; `#NUM!` basin 116/116 | G6-05 |
| **PRICE/YIELD/ODDF\*/DURATION** | `excel_bond_pow`: binexp for integer exponents, x87 `exp(RN53(RN64(y·ln x)))` for fractional | G6-03x |

**The decisive contrast:** at *identical* exact `tau`, `EXPON.DIST` yields the Kahan value and PMT does not.
PMT's `expm1` is a distinct routine. Harvesting FV's own `P` and `tf·q` from the closed FV oracle and feeding
them into `−(pv·P+fv)/(tf·q)` scores **0/109** at small rate, proving PMT does not share the forward annuity
factor either. PMT's discount routine is private to the PMT family.

---

## PART III — THE OPEN RESIDUAL, PRECISELY

### 8. The `em` oracle (the central instrument — understand this before anything else)

**Goal:** observe the exact `double` that Excel's internal `em = (1+r)^-n − 1` takes, without assuming any
model of the surrounding combine.

**Mechanism.** Choose `r = 2^-k`. Then in `pmt = ((num/em)/tf)·r`, the final `·r` is an **exact** scaling (a
power of two), and with `fv=0, type=0` we have `tf=1` and `num=pv`. So

```
pmt(r=2^-k, n, pv, 0, 0) = 2^-k · RN(pv / em)
```

Sweeping **128 consecutive `pv` values** massively over-determines `em`: each `pv` constrains `em` to an
interval, and 128 consecutive ones intersect to a single `double`. This is **model-free** — it assumes nothing
about how `em` is computed, only the (independently proven) combine shape. At general `r` the same technique
still uniquely pins ~90% of rows.

**Corpus.** `k = 1..24` × `n ∈ {1,2,3,4,6,8,12,16,24,32,64}` = **234 rows**. For each row we hold Excel's exact
`tau`, `u = EXP(tau)`, `lnu = LN(u)` (live captures, independently verified) and the pinned `em`.

**Why this is confound-free.** At exactly-representable `1+r`, `log1p(r) = ln(1+r)` with no argument rounding,
and the worksheet `LN` oracle is correctly-rounded on 148/148 such points. So `tau` carries no log1p confound.
Separately, at `|tau| ≥ 1` the branch `em = u−1` is exact (100%, 3840/3840 rows), which gives a *second*
confound-free window testing `log1p` alone.

### 9. Model scores on the 234-row oracle

| Model | Score | Note |
|---|---|---|
| All-double Kahan `RN53((u−1)·tau / ln u)` | **163** | the Goldberg/Kahan compensated form |
| **x87 spill-loop Kahan** (`fl53(fl64(·))` per op) | **165** | **best known; = production `excel_expm1_internal`** |
| Correctly-rounded `expm1(tau)` (mpmath prec200) | **128** | **ceiling proof — see below** |
| fdlibm `s_expm1.c` full | 129 | |
| Boost | 103 | |
| Cephes | 84 | |
| Real-hardware `F2XM1` direct (`2^y−1`) | 133 | the "too-accurate" un-rounded regime |
| Fully-extended chain from `(r,n)`, store once | 133 | same regime |
| Plain `u − 1` | 14 | no Kahan correction — refuted |

**The ceiling proof is the single most important structural fact in this lane.** Correctly-rounded `expm1`
matches only **128/234**. Any smooth function of `tau`, correctly rounded, is bounded by that; a polynomial
adds its *own* uncorrelated evaluation rounding and can only do worse. Empirically fdlibm (129) misses 105
rows, 103 of which are the same rows CR misses. **Therefore `em` is not an approximation of `expm1` in `tau`
at all.** It is the compensated Kahan reconstruction *riding on the x87 `exp`'s own rounding error* — which is
precisely why 165 > 128. Any future proposal that is "a better polynomial in `tau`" is refuted before it is
tested.

### 10. The 71 misses — signatures

- **Direction:** 57 toward-zero (Excel's `|em|` smaller than the model's), 14 away, 2 with `|offset| > 1 ULP`.
- **Required perturbation:** for 57 rows the denominator would have to be exactly `lnu + 1 double-ULP` (more
  negative), uniformly. Not a sub-ULP extended effect — a *different `double`*.
- **Not single-valued:** because 14 rows want the opposite direction, no single-valued `D(tau)` fits all 234
  rows → the discrepancy is **not denominator-only**.
- **The two `>1 ULP` rows are the sharpest fact.** No rounding of a *correct* `ln` can be more than 1 ULP from
  the CR value. Those two rows therefore **formally refute the entire faithful-rounding-variation class** in
  one stroke. Whatever generates `em` is not "the same computation rounded differently".
- **D-histogram:** the exact real Kahan quotient of the pinned operands rounds (RN) **correctly to our value**
  on 66/69 misses, sitting ~0.49–0.50 ULP from the midpoint — Excel returns the *neighbor*. The deciding
  information is a sub-ULP upstream difference **not present in any worksheet capture**.
- **Signed drift:** monotone `+0.585 → −0.324` ULP across `|tau| ∈ [1e-6, 1]`, sign-crossing — a *minimax
  error* fingerprint (smooth, coefficient-like), not a rounding-mode artifact.
- **Correlate (treat with suspicion):** misses concentrate where `tau = −n·log1p(r)` is *exactly
  representable* (68/71). **Likely a confound** — exact-`tau` is the `n = 2^j` subset, which occupies different
  `tau` strata, and any smooth drift correlates with a covariate that shifts the `tau` distribution. Fable's
  recommended test (**not yet run**): jointly regress miss/match on (`|tau|` binade, `|R − midpoint|`,
  `tau`-exactness) and check whether exactness retains explanatory power. Do this before building anything on
  the predicate.
- **Not branch-shaped:** the misses interleave with matches across `tau`; no threshold predicate separates
  them (confirmed independently by the enumerator's branch-mining, §14 EXT2).

### 11. The other residual (separate problem, do not conflate)

At `|tau| ≥ 1`, `em = u−1` is exact and PMT is still ~15% wrong on some corpora, with broad `−30..+17` ULP
misses concentrated in the `fv ≠ 0` / `type = 1` assembly. `race_combine_bigtau` found **no combine
arrangement beats the landed one** there. Current read: composed-chain faithful rounding (~0.502 ULP)
amplified by large `fv`, not a combine-shape error. This is the *next-cleanest* target if the `expm1` wall
stays shut — it is a different problem with more structural freedom.

---

## PART IV — HOW IT HAS BEEN APPROACHED

### 12. Phase history (what was tried, in order, and what it taught)

**Phase 1 — parametrized family racing (W108/early W109).** Enumerate {pow-provider × combine × store-mask}
and score. Peaked at 495/875 held-out. **Lesson: overfitting is the default failure mode.** The 36/48
single-corpus champion scored 32/48 on train under the best-held-out mask — a store-mask overfit. This
produced the standing rule in §19.

**Phase 2 — metamorphic siblings.** Harvest shared intermediates from *closed* sibling functions (FV/PV) and
inject them. Result: 0/109 → proved PMT does **not** share the forward annuity factor. Turned an unobservable
intermediate into an observed one and collapsed the hypothesis space. **Reusable and high-value.**

**Phase 3 — confound-free oracles and two retractions.** Built the `|tau| ≥ 1` window (where `em = u−1` is
exact so *only* `log1p` matters) and the `r = 2^-k` `em` pin. These killed two of my own "breakthroughs"
(§16). **Lesson: when a metric moves, first rule out the confound.**

**Phase 4 — inverse interval solve.** Rather than enumerate forward, invert: `em` is pinned, so back-solve the
exact rational interval each row's denominator/numerator must have occupied. Produced the §10 signatures and a
*certified target curve*, which forward search can never give. **The single best diagnostic built in this
lane.**

**Phase 5 — the "different ln implementation" class.** The insight that every prior test varied *rounding of
the same* `FYL2X` curve, never a *different error curve*. Tested: constant-chain `log10(u)·LN10` (direction
correct — `LN10` is +0.9 ULP high — but overshoots: shifts 143 rows, not 57); fdlibm `log1p`, fdlibm
`__ieee754_log`, Cody & Waite ALOG-1980 (all faithful ≈ CR, **symmetric** ±1 scatter). **Structural conclusion:
a faithful minimax log is bias-centered and therefore cannot produce a one-signed 57-row shift.**

**Phase 6 — new-observability hunt.** Search for a worksheet function that computes PMT's discount `expm1`
*directly as its result*. Captured fresh grids: EFFECT, RRI, EXPON.DIST, PV/FV (§7). **None use it.** PMT's
routine is private to its family; the `r=2^-k` pin is the only window, and it yields `em` but not the internal
intermediates.

**Phase 7 — the actual exhaustive enumerator.** Described fully in §14. Replaced hand-picked hypothesis
testing with bottom-up value-vector enumeration.

### 13. Two design reviews from Fable that changed the plan materially

Recorded because they encode real corrections, not opinions:

1. **Layer correction.** The proposed "(C source × compiler transform)" search space is nearly *empty* for the
   body, because 64-bit Excel means MSVC x64 means no x87 in compiled code. Reassociation, FMA formation, CSE,
   and constant materialization all drop out. The real space is
   `(op-tree) × (per-node provenance tag) × (transcendental delivery convention)`.
2. **Unsound-inverse correction.** "Exact-inverse meet-in-the-middle" (`A·B = em → A = em/B`) is **wrong in
   floating point**: `em` is the *rounded* root output, so the preimage is a half-ULP *interval* (~2^11 extended
   values per row), not a point. Exact-inverse MITM is a false-negative generator. The sound replacement is
   goal-directed **interval joins** with exact verification, depth ≤ 2.
3. Also flagged as unsound: **magnitude/interval pruning of intermediates** (`FSCALE`, `div`, `F2XM1` can move
   any magnitude into range in one or two ops). The only sound prunes are NaN-absorption and identity skips.

### 14. The enumerator (current state of the art in this lane)

`smart-fuzzer/tools/calc_graph_racer/src/bin/optree_search.rs` (+ `optree_foundation.rs` for the substrate gate).

**Engine.** Bottom-up value-vector enumeration with observational-equivalence dedup. Every program is
represented by its `[Ext80; 234]` value-vector; level `s+1` applies all ops to pairs from lower levels; dedup is
a 128-bit hash of the **full 234-row vector**. This natively covers **DAGs**, not just trees (both children draw
independently from the bank, so shared subexpressions are free). Recognition is automatic: a vector either
equals the target or does not.

**Leaf set L.** `{1, 0.5, 2, r, n, −n, ln2, l2e}` plus the intermediates in **both provenances**: `tau, u, lnu,
a = u−1` as spilled doubles, and `tau, u, w = F2XM1(f), a, lnu` as 80-bit resident values. 18 leaves.

**Op set O.** `+ − × ÷` in **both** SSE2 (`RN53` of exact) and x87 (`RN64`) flavors; `FYL2X`, `FYL2XP1`,
`FSCALE` (binary); `F2XM1`, `FRNDINT`, `chs`, `spill_RN53`, `spill_RZ53` (unary). All real hardware, all
domain-guarded.

**Soundness controls.**
- Substrate gate: reproduces the three known trees exactly — pure-SSE2 **163**, x87 spill-loop **165**,
  fully-resident **133**. If this gate ever fails, every result below is void.
- Join self-test (`SELFTEST=1`): inject a known-reachable size-3 target; the join must find it. **Passes.**
- NaN-absorption prune only (sound: NaN is absorbing under O, `em` is finite everywhere).

**Results — all negative.**

| Mode | Coverage | Result |
|---|---|---|
| Flat bank | size-1 = **1,025**, size-2 = **104,454** distinct | no hit |
| Root interval join | **size ≤ 5, arithmetic root** | **no hit** |
| EXT5 streaming size-3 | **size ≤ 3, ANY root** (incl. transcendental/spill) | **no hit** |
| EXT3/4 interval decomposition | quotient with one side fixed + **size ≤ 5** other side | **no hit** |
| EXT1 free-constant synthesis | one synthesized foreign constant, any size ≤ 2 subtree + outer op | **no hit** |
| EXT2 branch mining | 2-tree OR-cover | best **196/234** — no cover |
| EXT6 (running) | **size ≤ 7** via provenance-backed size-3 bank (**12,523,546** distinct size-3 vectors) | pending |

**The defensible claim as of now:**

> Over leaf-set L and op-set O above, Excel's `em` on the 234 pinned rows is reproduced by **none** of:
> size-≤3 any-root DAGs; size-≤5 arithmetic-root DAGs; quotients with a fixed evidenced side and a size-≤5
> other side; a single synthesized foreign constant; or a 2-branch composition of size-≤2 subtrees.
> **Therefore the generator is larger than these bounds, uses ≥2 foreign coefficients, or has a structure
> outside this frame.**

That is a bounded, quantified statement with L, O and the size limits explicit. **It is not** — and must never
be restated as — "no op-tree can reproduce the bits". Excel's own code is a reproducing op-tree; its existence
is certain. The gap is search reach, not existence.

### 15. Runner instrumentation (fixed 2026-07-25 — know this before re-running)

The first EXT6 run was killed after ~19 hours having produced **zero** durable output: stdout was pipe-buffered
through `grep`, there was no checkpoint, and the join was intractable because it materialized a 234-element
`Vec<Ext80>` per candidate. Fixed:

- **Flushed logging** to `smart-fuzzer/work/w109/G6-solvers/optree_search3.log` (`writeln!` + `flush()` per
  line, mirrored to stdout).
- **Checkpointed size-3 bank** at `optree_size3_bank.bin` — provenance triples `(op, a, b, dbl, row0)` at 18
  bytes/entry (~225 MB), *not* full vectors (which would be 23 GB). Reloaded automatically on restart.
- **Row-wise verification with early exit** (`eval3_row`): candidates are checked row by row and abandoned on
  the first mismatch, so a typical candidate costs 1–2 x87 ops instead of 234. This is the change that makes
  the size-≤7 join feasible at all.
- **Sharded, resumable join**: `SHARDS=n` (default 400), `SHARD_START=k`. Progress logged every 10 shards, so
  a kill loses at most one shard and the cleared prefix is recorded.

---

## PART V — RETRACTED CLAIMS (DO NOT RE-CHASE)

### 16. Every one of these was mine, was wrong, and cost cycles

1. **"Excel's PMT `log1p` is non-CR / faithful."** FALSE. `log1p` **is** correctly-rounded (= x87 `FYL2XP1`,
   bit-identical to CR software on 0/1350 confound-free rows). The apparent `+30` heldout gain from `std ln_1p`
   was pure **compensation** for the expm1 wall (`std − CR = +32` in the confounded `|tau| < 1` region, `−2` in
   the clean `|tau| ≥ 1` region). **Do not swap production `excel_log1p`.**
2. **"`em` is not a function of `tau_double` — the argument is kept extended."** FALSE. A designed collision
   probe appeared to show variation at fixed `tau`, but the configs shared `tau_double` *only under mpmath-CR
   `log1p`*; under a C-library `log1p` they have 3–4 distinct `tau_double` per group. A design artifact. The
   observed variation was the expm1's own ±1 ULP noise (impurity floor ~33 for *every* faithful candidate).
3. **"Excel's internal `log1p` spilled to double is faithful-not-CR."** FALSE — refuted by the confound-free
   `|tau| ≥ 1` oracle.
4. **"expm1 SOLVED 87/87."** Overfit — the 87 points did not stress `|tau| < 1`. The `po2 × n` corpus is the
   held-out that exposes the 70% ceiling.
5. **"The `+2` (163→165) comes from an RN64 numerator."** Unreproducible. The real mechanism is the **x87
   spill-loop** discipline (`fl53(fl64(·))` per op). Register-resident PC64 scores **145**, i.e. *worse*.
6. **"A proven irreducible boundary."** Over-claim (mine, 2026-07-24). At that point only ~dozens of
   hand-picked hypotheses had been tested — not a search. Corrected by building the enumerator; the honest
   form of the claim is §14's bounded statement.

The meta-lesson, which should be applied aggressively to any new result in this lane: **a "breakthrough" that
arrives without a confound-free control is probably a confound.** Three of the six above were exactly that.

---

## PART VI — ASSETS ON DISK

### 17. Data (`smart-fuzzer/work/w109/G6-solvers/`, gitignored — large)

**The critical ones:**

| File | Contents |
|---|---|
| `expm1_intermediates.csv` | **THE core corpus.** 234 rows: `k, n, tau_bits, u_bits, lnu_bits, em_pinned, em_aprod`. Excel's exact captured `tau`, `u`, `lnu` + the model-free pinned `em`. Every enumerator and racer reads this. |
| `em_consolidated.csv` | 324 rows: `src, r_bits, n, tau_bits, em_pinned, kahan` — 234 `po2n` + **90 `gen`** (general odd `m·2^-k` rates). The `gen` rows are the **lattice-overfit validation gate**. |
| `answers-pmt-po2n.json` / `batch-pmt-po2n.json` | The `r=2^-k × n` PMT sweep the 234 pins were solved from. |
| `answers-pmt-heldout.json` | Fresh held-out PMT corpus — the promotion gate. |
| `answers-pmt-combsweep.json` | 2304-row combine sweep; **100%** under the landed op-graph (this is what pinned the combine). |
| `answers-pmt-genrate.json` | 12,672 general-rate PMT witnesses. |
| `answers-pmt-{fvty,fv1sweep,fvsweep}.json` | `fv ≠ 0` / `type = 1` corpora — the *other* residual (§11). Note `fvsweep` is **degenerate** (constant across 256 pv) — do not score on it. |
| `answers-pmt-collide.json` + `collide-meta.json` | The designed-collision probe from retraction #2. Kept as a cautionary artifact. |
| `answers-em-exp.json` / `answers-em-ln.json` | Live `EXP(tau)` / `LN(u)` captures — verified identical to the CSV's `u`/`lnu` columns. |
| `answers-expondist.json` | `EXPON.DIST` = direct read of the *statistical* `expm1`. |
| `answers-effect-grid.json`, `answers-rri-grid.json` (+ batches/meta) | The observability-hunt grids (§7). Also expose two **open discrepancies** in OxFunc's own EFFECT/RRI — see §21. |
| `optree_size3_bank.bin` | Checkpointed size-3 provenance bank (written by EXT6). |
| `optree_search3.log` | Flushed progress log for EXT6. |
| `WORKFLOW_RESULTS.md`, `WORKFLOW2_RESULTS.md`, `COORDINATOR_NOTES.md` | Multi-agent campaign digests. |

### 18. Tools (`smart-fuzzer/tools/`)

**Oracle runner** — `Run-W109BulkBatch.ps1 -Batch in.json -Out out.json [-NoCache]`.
Bulk live-Excel capture through a recalc sheet, ~900 probes/s warm. **Invariant that must not be broken:**
argument doubles reach the function through **cell references** written via `Range.Value2`, never serialized
into formula text as decimal literals. `-NoCache` forces fresh computation (the bit-identity validation gate).
Batch format: `{function, row_id, probes:[{probe:{id, args:["0x<hex bits>", ...]}}]}`;
answers: `{function, witnesses:[{id, args, expected_bits}]}`.

**Racers** — `smart-fuzzer/tools/calc_graph_racer/src/bin/` (168 binaries; run with
`cargo run --release --bin NAME` **from the crate directory** — a common mistake is running from the repo root,
which fails since it is a standalone workspace).

The ones worth knowing:

| Binary | Purpose |
|---|---|
| `optree_search.rs` | **The enumerator.** Flat envelope + root interval join + EXT1–EXT6. Env: `SELFTEST=1`, `SEARCH3=1`, `SHARDS=n`, `SHARD_START=k`. |
| `optree_foundation.rs` | Substrate + correctness gate (163/165/133) + bank-growth measurement. **Run this first after any change to the x87 layer.** |
| `race_pmt_prod_vs_fix.rs` | Production op-graph vs candidate variants across all corpora. The landing scoreboard. |
| `race_log1p_id.rs`, `verify_log1p_split.rs`, `race_log1p_general.rs` | The `log1p = CR` proof, incl. the confounded/clean split. |
| `doubt_combine.rs`, `race_collide_search.rs`, `race_combine_spill.rs`, `race_combine_bigtau.rs` | Combine-shape identification (7 forms) and its `|tau| ≥ 1` re-test. |
| `race_spill_kahan.rs`, `race_kahan_sched.rs`, `race_spill_exhaustive.rs` | The 163→165 spill-loop discipline; 9216-config schedule search. |
| `race_extdenom_em.rs`, `race_uext_denom.rs`, `race_numtauext.rs`, `race_fullext_em.rs` | Operand-provenance isolations (extended denominator / numerator / full chain). |
| `race_chop_em.rs` | Directed-rounding tests **+ the inverse-solve diagnostic dump** (required per-row perturbation). |
| `race_log1pden_em.rs` | `FYL2XP1(u−1)` vs `FYL2X(u)` denominators — proves they are bit-identical. |
| `race_reassoc_em.rs` | All associations of the two multiplies and one divide. |
| `race_f2xm1_direct.rs`, `race_binexp_em.rs` | Hardware `F2XM1` direct; binexp discount factor. |
| `race_lnvia_log10.rs` | The `log10·LN10` constant-chain (Fable A1). |
| `dump_expm1_intermediates.rs`, `export_em.rs`, `agentC_emdump.rs` | Corpus construction from the pinned oracle. |
| `diag_em_nature.rs`, `diag_pmt_misses.rs` | Residual-structure diagnostics. |
| `race_effect_rri_check.rs` | Scores OxFunc's EFFECT/RRI against the fresh grids (§21). |

**Analysis** — most fingerprint sweeps (fdlibm/Cody-Waite/Cephes log donors, association forms, free-constant
checks) were done in throwaway Python against `expm1_intermediates.csv`. Python's `float` is IEEE-754
`binary64` with RN, so plain-double models are exact there; **anything involving 80-bit must go through the
Rust x87 layer** (or `mpmath` at `prec=64` then `float()`, which is emulable but slower and easier to get
wrong).

### 19. Docs

- `docs/notes/PMT_EXPM1_IDENTIFICATION_STORY.md` — narrative field diary, incl. dead ends. Keep appending.
- `docs/function-lane/W109_G6_PMT_RESUME_20260723.md` — earlier resume (accurate, narrower).
- `docs/function-lane/W109_G6_BOND_SCHEDULE_IDENTIFICATION_20260720.md` — Lane D holds the PMT history.
- `docs/OXFUNC_EXCEL_DISCREPANCY_CATALOG.md` — **canonical** tracker; row G6-01 carries the full ledger.
- `docs/notes/WELINDER_GNUMERIC_EXCEL_MINING.md` — mined public-source digest (no financial coverage, but the
  FP-constant representation analysis is directly reusable and generated hypothesis A1).

---

## PART VII — IDEA LEDGER

### 20. Explored and refuted (do not repeat without a new reason)

**Substrate / precision:** register-resident PC64 (145) · fully-extended from `(r,n)` (133) · extended
denominator via `FYL2X` kept 80-bit (123) · extended-`tau` numerator (142) · mixed provenance `ln(u_ext)`
(24 — and *catastrophic*: differs from captured `lnu` by up to ±131072 ULP because `ln` is hypersensitive to
`u`'s low bits at `u ≈ 1`, which **proves `u` must spill to double before the log**) · PC=53 control word (151)
· all 9216 spill schedules (max 165).

**Rounding modes:** final-divide chop RZ (112) · numerator chop (120) · RZ64→RN53 (120) · whole-schedule
directed rounding (112–130).

**Op-graph shape:** all associations of `(u−1)·tau/lnu` (119–145) · additive-correction split
`a + a(tau−lnu)/lnu` (145) · double-divides `a/(lnu/tau)` (129), `tau/(lnu/a)` (120) · expanded
`(u·tau−tau)/lnu` (13) · reciprocal-multiply combine (0 configs) · forward-exp combine (worse everywhere) ·
`v = exp(tau)` instead of `1+em` (slightly worse on fvty).

**Alternative primitives:** hardware `F2XM1(tau·log2 e)` direct (133) · `fFEXPM1` `−w·m` assemble (115) ·
`w`-based numerator (7) · binexp discount factor `1/(1+r)^n` (differs on 60 rows; `em == v−1` only 13,
Kahan(v) 134) · plain `u−1` (14) · classic positive-power PMT e2e (42–51%).

**Polynomials:** CR `expm1` (128 — the ceiling) · fdlibm (129) · Boost (103) · Cephes (84) · exact-Taylor
Horner deg 3–16 (19→111, plateaus at 103 for K0) · Estrin ordering (±2, associativity unlocks nothing) ·
global LSQ/Chebyshev fits (0–21: a real `expm1` poly needs `a1` *exactly* 1.0 and `a2` *exactly* 0.5, and any
fitted `a1` destroys every small-`|tau|` row).

**Different ln implementations:** `log10(u)·LN10` (direction right, overshoots — 143 rows shifted vs 57) ·
`log2·LN2` (wrong direction: `LN2` is low) · `log2/LOG2E` (too weak, 0.06–0.13 ULP) · fdlibm `log1p` (225/234
identical to captured) · fdlibm `__ieee754_log` (228/234 identical) · Cody & Waite ALOG-1980 (176/234, ±1
**symmetric**). Structural conclusion: **faithful minimax logs are bias-centered and cannot produce a
one-signed 57-row shift.**

**Observability:** EFFECT, RRI, EXPON.DIST, PV/FV all use *different* kernels (§7) — no sibling exposes PMT's
`expm1`.

**Provenance:** Welinder's blog has no financial coverage. John D. Cook / general literature confirm the public
technique for `(1+r)^n − 1` cancellation-avoidance is exactly `expm1`/`log1p` — which is what OxFunc already
does. No public source describes Excel's bit-level annuity routine.

**Enumeration:** §14's six modes.

### 21. Considered but NOT yet explored

Ordered by my estimate of value per unit effort.

1. **The exactness-predicate regression (10 minutes, highest value/effort).** Jointly regress miss/match on
   (`|tau|` binade, `|R − midpoint|`, `tau`-exactness). If exactness survives as an independent predictor,
   that implies a **branch or early-out in the code** (e.g. `if (u == 1.0) return t;`, or an `exp` shortcut for
   trailing-zero mantissas) — a genuinely new structural hypothesis. If it does not survive (my prediction),
   the predicate is a confound and should be struck from the record so nobody builds on it again.
2. **Finish EXT6 and then EXT7 = interval decomposition at size 3 per side.** The decomposition mode (§14
   EXT3/4) currently searches the free side to size 5 using the size-≤2 bank. Re-running it against the
   *size-3* bank lifts each side to size 7, i.e. quotient trees of effective size ~15 — Fable's estimate for
   where a genuinely different internal reduction would live. The checkpointed bank makes this cheap now.
3. **Coefficient recovery as exact constraint solving — the highest-value unbuilt tool.** This is the right
   mechanism whenever a hypothesised form carries unknown constants, and it is a *solve*, not a fit or a blind
   search. Suppose `em = RN53(N / D)` with `N` pinned and `D = Σ cᵢ·zⁱ` a polynomial/rational in a known
   reduced argument `z`. Two facts make this tractable:
   - Each pinned row converts an *equality on bits* into an **exact interval on `D`**: `RN53(N/D) = em`
     confines `D` to a half-ULP dyadic interval whose endpoints are exact rationals (computable in `i128`
     dyadic arithmetic, no floats).
   - `D` is **linear in the coefficients `c`**.

   So the hypothesis becomes **234 exact linear interval constraints in `k` unknowns** — a linear feasibility
   problem, solvable exactly in rational arithmetic. Widen each interval by a sound bound on the floating-point
   evaluation error of the candidate evaluation order (a few ULPs for degree-`d` Horner) to obtain a
   *relaxation*: infeasibility of the relaxed system is a **proof that the form is refuted**, and a non-empty
   feasible polytope is a small candidate region to verify exactly, coefficient by coefficient.

   With `k ≲ 6` this is over-determined by ~228 constraints, so recovering `c` is **identification, not
   interpolation** — the MINVERSE overfit lesson does not apply here and must not be mis-invoked to avoid the
   work. What *is* worthless is assigning 71 free values to the 71 miss rows (zero constraint, guaranteed
   "fit", no predictive content); the distinction is parameter count against constraint count, nothing else.

   Run it for: the fdlibm / Cody-Waite / Cephes log *forms* with their coefficients freed (the forms were
   tested, the coefficients never were); `ln2_hi`/`ln2_lo` split constants; a general degree-3..8 minimax
   denominator; and the same treatment applied to the numerator. Validate any feasible region against the 90
   general-`r` rows and a fresh oracle batch before believing it. Note EXT1 (§14) is the `k = 1` special case
   of exactly this, already implemented and negative — generalising it to `k > 1` is the natural next build.
4. **The `|tau| ≥ 1` / `fv ≠ 0` residual (§11).** Different problem, more freedom, ~15% of a real corpus, and
   entirely untouched by the enumerator (which targets `em` alone). Probably the best *expected value* target
   in the whole lane if the goal is "reduce total divergence" rather than "close `em`".
5. **General-`r` `em` pinning at scale.** We have 90 `gen` rows in `em_consolidated.csv` but only the 234
   `po2n` rows carry captured `u`/`lnu`. Capturing `EXP`/`LN` for the general-`r` rows would produce a second
   confound-free corpus on a *different* mantissa lattice — the single best defense against the possibility
   that everything so far is a `2^-k`-lattice artifact.
6. **IPMT/PPMT/CUM\* internal structure.** Assumed to inherit PMT and otherwise be simple, but the naive
   `IPMT == RN(FV(per−1)·r)` was **refuted live (0/9)**, so the balance recurrence has its own unidentified
   staging (per-period vs closed-form FV), and CUM\* has an unidentified fold order. These are *independently
   closable* and currently unexamined. Good ROI.
7. **x87 exception/precision-flag effects.** Never examined. Denormal handling, `FSTP` with pending exceptions,
   or a non-default MXCSR/CW inherited from a caller could shift a last bit. Low prior, cheap to probe.
8. **Whether `tau` itself is formed differently.** We assume `tau = −n·log1p(r)` with `n` as a `double`
   multiply. Alternatives never tested: `tau` accumulated by repeated addition of `log1p(r)` for small integer
   `n` (a period-typical idiom, and it produces *different* last bits than a multiply), or `n·log1p(r)` with a
   sign applied at a different point.
9. **Period-toolchain confirmation lane.** Compile candidate C with an era MSVC against era CRTs (the SxS
   harness from the chopped-exp hunt exists) and run on the real FPU. This is a *confirmation* tool for a
   winning candidate, not a search tool — but it is the strongest possible corroboration if a hit ever appears.
10. **Publication-shape re-examination.** We assume the pinned `em` is the routine's return value. It could be
    a value that has already passed through one publication step, in which case we are searching for the wrong
    target by one op. The root interval join partially covers this (`spill` is an op), but an explicit test —
    "is `em` itself the output of a chop/RN wrapper applied to a cleaner value?" — has not been done as such.

---

## PART VIII — METHODOLOGY, EMPHATICALLY

### 22. The one guideline that matters most: symbolic execution, not statistics

**Do not drive this search with match counts.** "Candidate X scores 163/234, candidate Y scores 165/234" is
almost worthless as a *search signal*, and actively misleading as evidence. Three reasons, each learned the
hard way here:

1. **Scores are dominated by rows the model gets right for structural reasons**, so a 2-row difference between
   two candidates is noise relative to the ~160 rows they share. Optimizing that difference is how retraction
   #4 (the "87/87 solve") and the Phase-1 store-mask overfit happened.
2. **A higher score can be pure compensation.** `std ln_1p` gained +30 held-out rows *by cancelling a different
   error*. It looked like progress and was a wrong turn. In the clean region it was −2.
3. **The generator is deterministic and exact.** There is no "closeness" to exploit. Either a program produces
   the exact 234-vector or it does not. Ranking near-misses ranks *coincidences*.

**What to drive with instead:**

- **Trace the deterministic computation symbolically.** For a specific row, write out the exact sequence:
  which value enters which instruction, at what precision, rounded when, stored where. Compute the *exact real*
  intermediate (rational or `mpmath` at high precision) and identify precisely which operation's rounding
  decision differs from ours, and by how much relative to the midpoint. `race_chop_em.rs` does this and its
  output (the per-row required perturbation) generated every real insight in Phase 4.
- **Use the signed residual's structure.** Smooth drift ⇒ coefficients (Gauss-Newton territory). High-frequency
  ⇒ op-graph/rounding. Sign-crossing equioscillation ⇒ minimax approximation error. Concentration in a `tau`
  band ⇒ a branch or a reduction boundary. The residual is a *deterministic signal*, never noise.
- **Prove impossibility on the cleanest few bits.** The strongest results in this lane are of the form "this
  entire class cannot produce this observation" — e.g. the CR ceiling (§9), the symmetric-scatter argument
  against faithful logs (§12 Phase 5), the two `>1 ULP` rows killing the rounding-variation class (§10). One
  such argument is worth a thousand scored candidates.
- **Isolate the link directly.** Do not back-solve which link of a composed chain failed. Find the input that
  *collapses* the chain (exactly-representable `1+r` makes `log1p` exact; `|tau| ≥ 1` makes `em = u−1` exact;
  `r = 2^-k` makes `·r` exact) and query the suspect primitive against a direct oracle. Every retraction in
  §16 was resolved this way.

### 23. Supporting rules

- **Confound-free control, always.** Before believing any improvement, identify what else changed. The expm1
  wall is present in *every* general-rate corpus and will silently absorb or amplify unrelated effects.
- **Held-out before promotion.** Score the *whole candidate family* on a fresh disjoint corpus. If the ceiling
  is well below 100% **and** the best-held-out candidate differs from the best-train candidate, the champion is
  an overfit and the true op-graph is outside the family. Non-negotiable before any landing.
- **Doubt probes.** Periodically re-verify things "known". This caught retractions #2, #3 and #5. Specifically
  re-verify: that a captured intermediate really is what we think; that an oracle's invariant holds under the
  *same* routine the target uses; that a two-step emulation is not double-rounding where hardware does one step
  (a real bug found in `race_spill_exhaustive`: `ln(u) = fyl2x(1,u)·ln2` double-rounds where `fyl2x(ln2,u)`
  does not).
- **Over-determine, never sparse-fit.** 128 *consecutive* `pv` to pin one `em`, not 8 scattered ones. Two-free-
  parameter interval fits reached ~80% on **mismatched-wants controls** — always run a mismatched control.
- **Never write "production ready"** (standing instruction).
- **Bank narrative material as it happens** into the story note and `ExcelFunctionsHandbook/content/lastbit/`
  — dead ends included; they are the most useful part of the record.
- **Session transcripts** archive to the private repo `DnaCalc/OxFunc-History`, **never** into public OxFunc.

### 24. Known open discrepancies surfaced in passing (separate lanes, real bugs)

From the observability hunt, with oracle grids already captured and a scorer written
(`race_effect_rri_check.rs`):

- **EFFECT** misses 10/315 rows vs live Excel — a block at internal rate `r = 2^-8`, off by **+32…+76 ULP**,
  error growing with `npery`. Tens of ULP ⇒ the `(1+r)^n` accumulation *order* differs from Excel's; OxFunc's
  `power_kernel` binexp squaring order is not EFFECT's.
- **RRI** misses 3/154 **catastrophically** (`+2^27` ULP) when `fv ≈ 1`: `powf(fv, 1/n) − 1` loses half its
  bits to cancellation while Excel returns an accurate tiny result. `NOMINAL` shares the same `powf − 1` code
  shape and likely the same latent bug.

Both are ordinary identification problems with good odds of closing — unlike the `em` wall.

---

## PART IX — RECOMMENDED FIRST MOVES

For someone picking this up cold, in order:

1. **Verify the substrate.** `cd smart-fuzzer/tools/calc_graph_racer && cargo run --release --bin
   optree_foundation`. It must print 163 / 165 / 133. If not, stop and fix the x87 layer — every result in this
   brief depends on it.
2. **Read `race_chop_em.rs`'s output.** It prints the per-row required perturbation. That table is the actual
   shape of the problem; internalize it before generating hypotheses.
3. **Run the exactness-predicate regression** (§21 item 1). Cheap, and it either kills a confound or opens a
   branch hypothesis.
4. **Check EXT6's log** (`optree_search3.log`) and, if it completed negative, run the size-3 decomposition
   (§21 item 2) — the checkpointed bank makes it the cheapest remaining depth increase.
5. **If the `em` wall stays shut, switch targets** to the `|tau| ≥ 1`/`fv ≠ 0` residual (§11) or the
   IPMT/CUM\* internals (§21 item 6). Both are unexplored and independently closable, and closing them reduces
   real divergence — which the `em` last bit, at ≤1 ULP on ~30% of one internal value, does not do much of.

**Do not** re-run the refuted list in §20 without a specific new reason, and **do not** restate the bounded
negative in §14 as a universal one — it is a statement about how far the search has reached, nothing more.

The position to hold: a reproducing program exists (Excel runs it), we would recognise it instantly, and every
operand it consumes is already pinned. What is missing is reach — a larger size bound, a coefficient set
recovered by §21 item 3, a reduction we have not yet expressed, or an observation channel not yet built. Each
of those is a concrete, attackable object. Pick the one with the best ratio of reach gained to effort spent,
build it properly, and record exactly what it cleared.
