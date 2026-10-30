# W109: PMT intermediate and timing discrimination

Status: `in_progress`; G6-01 remains open

Investigation date: `2026-08-09`

This record consolidates the current-reference PMT intermediate, exactness,
period-product, hidden-low-word, and timing-factor investigations. It records
useful local identities and refuted candidate families, but it does not identify
an exact end-to-end PMT calculation graph and does not authorize a production or
formal-route change.

## Result and overclaim retraction

The evidence supports two narrower conclusions:

1. exact formation of the stored period product is strongly associated with
   misses of the ordinary Kahan-style `expm1` reconstruction in the combined
   324-row corpus, but this is a statistical discriminator, not an identified
   branch or early-out;
2. for power-of-two rates with `fv = 0`, the paired `type = 0` / `type = 1`
   worksheet outputs obey multiplication by the stored reciprocal of `1+rate`
   on all 832 available pairs. This is a local type-pair identity. It does not
   determine the annuity helper, general-rate timing order, or end-to-end PMT
   publication graph.

Any prior working claim that the bank contained 100 usable timing pairs is
withdrawn. A fresh audit of 18 PMT answer files found 67,066 eligible
power-of-two-rate, `fv = 0`, timing rows and 53,803 tuple keys, but only 64
prior-bank tuples had both timing outputs needed by this metamer. The current
832-pair score is therefore 64 prior-bank pairs plus 768 answer-blind,
bank-disjoint frozen pairs.

Any claim that the reciprocal result identifies the general timing-factor
graph is also withdrawn. On the frozen 480-call general-rate timing-order gate,
the best tested family reaches only `378/480`; it is exact on just one of 15
contexts and no candidate is exact across all contexts. Likewise, the
exact-period-product association is retained only as a probe-design hypothesis,
not as proof of a hidden Excel branch.

## Current-reference capture provenance

All four fresh answer files embed `w109-capture-provenance-v1` and agree on:

- Excel `16.0`, build `20228`, 64-bit;
- workbook Compatibility Version `2`;
- `Range.Value2` argument injection and `cell_value2_bulk` result capture;
- `Run-W109BulkBatch.ps1` runner version `w109-bulk-batch-v2`;
- `NoCache`, with cache hits `0` and misses `0`.

The serialized capture orchestration observed zero Excel processes before each
capture and zero after bounded teardown (`pre = 0`, `post = 0`). The JSON files
embed the application/CV/Value2/NoCache profile; the process counts are the
corresponding orchestration observations rather than fields in the answer JSON.

| answer cohort | function | rows/calls | captured UTC |
|---|---|---:|---|
| `answers-pmt-general-exp-20260809.json` | `EXP` | `90` | `2026-08-09T06:41:18Z` |
| `answers-pmt-general-ln-20260809.json` | `LN` | `90` | `2026-08-09T06:43:17Z` |
| `answers-pmt-tf-metamer-heldout-20260809.json` | `PMT` | `1,536` | `2026-08-09T07:22:22Z` |
| `answers-pmt-tf-order-discriminator-20260809.json` | `PMT` | `480` | `2026-08-09T08:03:28Z` |

These observations apply only to the named current-reference profile. The
distribution channel is not embedded in these artifacts and remains
unspecified. No alternate Excel channel/build, CPU architecture, or workbook
Compatibility Version result is inferred from them.

## EXP/LN intermediate capture and exactness predicate

`Generate-PmtGeneralIntermediateBatches.ps1` selected all 90 pre-existing
general-rate rows from `em_consolidated.csv`; it did not select rows from new
oracle answers. The first live batch captured `EXP(tau)`. The second batch then
used those exact captured EXP outputs as inputs to `LN`, preserving the
worksheet-level `LN(EXP(tau))` intermediate rather than replacing it with a
host-library approximation. IDs, arguments, counts, numeric bit strings, and
capture provenance are asserted by `analyze_pmt_exactness_predicate.py`.

The independently rerun audit reported:

| cohort | rows | plain Kahan exact | stored-x87 Kahan exact | exact-product rows | rounded-product rows |
|---|---:|---:|---:|---:|---:|
| power-of-two bank | `234` | `163/234` | `165/234` | `169` | `65` |
| general-rate live intermediates | `90` | `61/90` | `61/90` | `70` | `20` |
| combined | `324` | `224/324` | `226/324` | `239` | `85` |

For the combined plain reconstruction, exact-product rows miss `94/239`, while
rounded-product rows miss `6/85`. After one-hot controls for tau binade,
rounding-midpoint-distance octile, and corpus family, the exact-product
coefficient is `+3.107719820`, odds ratio `22.37`, likelihood-ratio
`chi2(1) = 54.806879130`, and `p = 1.32974516e-13`.

The general-rate cohort by itself is weaker: its adjusted odds ratio is
`3.72677` with `p = 0.0509659131`, which does not meet the script's stated
`p < 0.01` retention rule. The strong combined association is therefore a
useful discriminator shaped substantially by the power-of-two corpus. It does
not establish that Excel tests exactness, nor identify what Excel would do on
an unobserved row.

## Tau-formation and integer-discount negative racers

`race_pmt_tau_formation.rs` varied the construction of
`tau = -n * log1p(rate)` over the 234-row power-of-two bank while holding the
captured downstream intermediates fixed.

- ordinary multiply, stored-x87 multiply, ordinary binary addition, and
  stored-x87 binary addition all reproduce the captured tau bits on `234/234`;
- ordinary and stored-x87 repeated addition reproduce only `131/234` and are
  refuted as the universal tau-formation schedule;
- substituting any tested formation does not recover the pinned PMT
  intermediate: the best Kahan variant is `165/234`;
- the exact-product partition is `169/234` exact and `65/234` rounded, but the
  tested hybrid switches remain at most `165/234`.

The `234/234` agreement of multiply and binary-add schedules is observational
equivalence at the stored tau boundary, not instruction-level identification.

`race_pmt_integer_discount.rs` then tested stable integer-period recurrences in
the discount-minus-one domain, including binary composition under ordinary and
stored-x87 arithmetic, on all 324 power and general rows. The best enumerated
recurrence scores only `163/324` (`116/234` power, `47/90` general). This
refutes those enumerated recurrence families as exact explanations; it does not
exclude every possible private integer-period algorithm.

## Hidden TwoProduct low word and coefficient-family negative result

`analyze_pmt_lowword_coefficients.py` reconstructs the exact TwoProduct
residual of `n * log1p(rate)` and keeps coefficient recovery separate from the
90-row general-rate replay. Across the 324 rows, 239 have zero low word (the
exact-product cohort) and 85 have a nonzero low word.

Directly delivering the low word with coefficient one does not improve the
baseline into an exact graph. The ordinary and stored-x87 numerator-hi-plus-lo
forms score `222/324` and `224/324`, compared with baselines `224/324` and
`226/324`. The best recovered one-coefficient stored-x87 correction uses
`alpha = 0.68589206346580867` and reaches only `227/324`; its general-rate score
remains `61/90`.

The broader frozen coefficient search fits smooth Chebyshev corrections on the
234 power rows before replaying the 90 general rows. Every tested ideal interval
system requires positive widening: the smallest reported uniform slack is
`0.366799` relative-epsilon units. Among the listed least-squares joint
smooth-plus-low families, the best power replay reaches `190/234`, and the best
general replay reaches `61/90`; no family is exact on either the recovery bank
or the held-out general cohort.

Exact rational Farkas-certificate recovery succeeds for `51/60` enumerated
smooth interval systems. Nine systems still show positive floating-LP slack but
do not yield an exact certificate; those nine are numerical negative evidence,
not a formal infeasibility result.

Thus a single hidden TwoProduct low word and its enumerated delivery graphs are
hard-refuted by the immutable-row ceiling. The 51 certified smooth systems are
exactly infeasible, while the remaining nine tested systems have no exact replay
survivor but remain explicitly uncertified. This is a bounded negative result
over the enumerated families, not a proof that Excel never retains additional
precision.

## Power-of-two timing-factor metamer

For `fv = 0`, pair otherwise identical PMT calls at `type = 0` and `type = 1`.
At a positive power-of-two rate, the final multiplication by `rate` is an exact
exponent shift, allowing the unknown annuity helper to cancel from the local
relationship. The racer compares:

```text
reciprocal candidate = type0 * stored(1 / (1 + rate))
divide candidate     = type0 / (1 + rate)
```

The frozen generator used a fixed seed, excluded every banked PMT argument
tuple, and emitted 768 new type pairs (1,536 calls) before their answers were
captured.

| cohort | pairs | reciprocal candidate | divide candidate | discriminating pairs |
|---|---:|---:|---:|---:|
| audited prior bank | `64` | `64/64` | `55/64` | `9` |
| frozen held-out | `768` | `768/768` | `718/768` | `50` |
| combined | `832` | `832/832` | `773/832` | `59` |

This exactly identifies the local paired-output relationship on the observed
power-of-two domain and refutes direct binary64 division for the 59
discriminating pairs. It does not locate the reciprocal relative to the hidden
annuity helper or general-rate multiplication, and it is not an end-to-end PMT
replay.

## Frozen general-rate timing-order discriminator

`generate_pmt_tf_order_discriminator.rs` selected 15 answer-blind,
prior-bank-disjoint `(rate,nper)` contexts from disagreement among predeclared
candidate graphs. Each context contains a 16-value consecutive-PV ladder at
both timing values: 240 pairs and 480 calls. The generator deliberately ignores
its own answer file on deterministic reruns so that a post-capture rerun retains
the frozen batch.

`score_pmt_tf_order_discriminator.rs` treats the private annuity intermediate
`em` as a per-context nuisance parameter. A single fitted `em` must explain all
32 outputs in a context. It scores 18 pre-frozen operation families over native
and stored-x87 staging combinations; `q` below denotes the staged `pv / em`
quotient.

The best family is the subtractive stored-`r/tf` form:

```text
type 0: q * r
type 1: (q - q * stored(r / (1 + r))) * r
```

Its best representative scores `378/480`: `239/240` type-0, `139/240` type-1,
sum absolute ULP `110`, worst ULP `2`, and only `1/15` contexts exact. Several
staging masks tie at that score because their selected stores are
observationally equivalent on this gate. The next representatives include
`q*stored(1-stored(r/tf))*r` at `378/480`,
`q*r-(q*r)*stored(r/tf)` at `372/480`, continuous-PC64 `q*r/tf` at `360/480`,
and direct `(q/tf)*r` at `307/480`.

No frozen family yields an all-context or global exact graph. The result
therefore narrows future search toward subtractive `r/tf` associations while
leaving operation order, store sites, and the hidden annuity intermediate open.
No candidate was promoted to production from this score.

## Reproducible source inventory

The following source tools constitute the focused reproduction path:

- `smart-fuzzer/tools/Generate-PmtGeneralIntermediateBatches.ps1` — freezes the
  90-row EXP batch and derives the LN batch from captured EXP output bits;
- `smart-fuzzer/tools/Run-W109BulkBatch.ps1` and
  `smart-fuzzer/tools/CellRefBatch.psm1` — current-reference Value2/NoCache
  capture runner and cell-reference batch substrate;
- `smart-fuzzer/tools/analyze_pmt_exactness_predicate.py` — artifact validation,
  Kahan replays, and controlled exact-product likelihood-ratio audit;
- `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_tau_formation.rs` —
  tau-construction discriminator;
- `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_integer_discount.rs` —
  integer-period recurrence discriminator;
- `smart-fuzzer/tools/analyze_pmt_lowword_coefficients.py` — exact TwoProduct
  residual, one-coefficient recovery, and frozen coefficient-family replay;
- `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_pmt_tf_metamer_heldout.rs`
  and `race_pmt_tf_metamer.rs` — answer-blind power-of-two metamer gate and
  prior-plus-held-out scorer;
- `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_tf_order.rs` — exploratory
  model-free timing-order inverse-interval racer;
- `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_pmt_tf_order_discriminator.rs`
  and `score_pmt_tf_order_discriminator.rs` — frozen general-rate discriminator
  generator and nuisance-intermediate scorer.

The offline verification reruns used the Python analyzers and the four Rust
scorers directly; they made no Excel/COM calls and did not mutate the evidence.
Live recapture, if required, must remain serialized and use
`Run-W109BulkBatch.ps1 -NoCache` under the normal pre/post process-count guard.

## SHA-256 inventory

### Source and seed inputs

| path | SHA-256 |
|---|---|
| `smart-fuzzer/tools/Generate-PmtGeneralIntermediateBatches.ps1` | `8C2B912AC81FE6DAD5756F01F4FB44EEEC890CAB3E625D5D53336F616B602374` |
| `smart-fuzzer/tools/Run-W109BulkBatch.ps1` | `AEE87CAA1EDB4B26002522B414BF7F0C23A99C1131D0BF6D5F6C076A316064DF` |
| `smart-fuzzer/tools/CellRefBatch.psm1` | `0127DBE03CCB807C4DBAD5626ABED0A93B95EF012A2F479085D40E9F1D291CC3` |
| `smart-fuzzer/tools/analyze_pmt_exactness_predicate.py` | `E97E47AE72EC89EE0E7D990646F329A9B474DB5932EBD2765EBE87D6504EDF29` |
| `smart-fuzzer/tools/analyze_pmt_lowword_coefficients.py` | `26E6B61F401A72273D12FE5890279F9E814E838C1C1DEC9B9C277F221318B324` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_tau_formation.rs` | `4A8FCB1ADA366517E692BA46C6965AF98451519D883F4305759049089B44FFC3` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_integer_discount.rs` | `2DC2E375AE7805AC575A1B9CD3B98C03DA47DB635361DAEACF0078EE88505C02` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_pmt_tf_metamer_heldout.rs` | `28F7DC3A5249525FFDA28D18AAA9E8E55BF2F290F9358953CD090EF5EAA76950` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_tf_metamer.rs` | `D1DD68FBFA928D722C8365DE57F45FDE5F994CBC2337A1CF2F1989B0A7CA741E` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/race_pmt_tf_order.rs` | `358ABCFF728299D9CFD2445CEA6005C189C92EDD6CCD01A6C59DDF563F3566E3` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_pmt_tf_order_discriminator.rs` | `BD2EE1463DF8777D6EDEF0E1315888055942262DD45CE29EB1997FAAD788BC31` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/score_pmt_tf_order_discriminator.rs` | `074C217753D5A492E37CDFF3F858EC15A4884C5E539CD51BB5F31EA401A6B829` |
| `smart-fuzzer/work/w109/G6-solvers/em_consolidated.csv` | `83DDBB43D6D9A3EE56CF7364946F1434B1BC083FD788ECCF7216DD48175E7378` |
| `smart-fuzzer/work/w109/G6-solvers/expm1_intermediates.csv` | `81A3E37A25FD1CFD38F28599F1C647EF20E608BFA12B1AD27E88935D0728B3E6` |

### General-rate intermediate artifacts

| artifact | SHA-256 |
|---|---|
| `meta-pmt-general-intermediates-20260809.csv` | `C836B32D6B4BAE93ECE1B5D4E7362A48BEF2D90F416D492B4F6C447ADDE59A7B` |
| `batch-pmt-general-exp-20260809.json` | `CBFAB2DF07BF05EEAB74F9BEF6BE3C8B0E740A5E38B0A2B8DEA6A3DB48292284` |
| `answers-pmt-general-exp-20260809.json` | `397650FBE03136719B6A8112B66E61ADE7E926753423285DD763DBD32ABB58B6` |
| `batch-pmt-general-ln-20260809.json` | `1B82746268EE9ED93780A1AE2B4203611402A15FD80F8DBAA50174263A668A8F` |
| `answers-pmt-general-ln-20260809.json` | `0DBE490914FC9527DD13891314C33AD332D3CF792AB918F7BF9B98F5265EA1BC` |

### Power-of-two timing metamer artifacts

| artifact | SHA-256 |
|---|---|
| `batch-pmt-tf-metamer-heldout-20260809.json` | `6A88FD0E7B259261B2BF21C4667C94FCD999080B7820BE71E88EC0AE5E25B22E` |
| `meta-pmt-tf-metamer-heldout-20260809.csv` | `96DD5FD040BB8AADDE7EECDFC4B2D8921A3B030D8D260373E1455A9E681C93AE` |
| `answers-pmt-tf-metamer-heldout-20260809.json` | `305B6165FA3AB2014F748879208A510C49A93A4EC193DAAEB47730CEF3540957` |

### General-rate timing-order artifacts

| artifact | SHA-256 |
|---|---|
| `batch-pmt-tf-order-discriminator-20260809.json` | `13C51A9884C7762DB54B82CAB182B875001AE85C6D61D33D29D045613E132C33` |
| `meta-pmt-tf-order-discriminator-20260809.csv` | `98B2E894BC90790788E2429C0C15955F4295525C5D44EEA83A757B478C2541F8` |
| `answers-pmt-tf-order-discriminator-20260809.json` | `0D44A7C5E4F47BFBC8015302D20FBBC6227CA6BF49BBAABC7FE7D7C7B805A751` |

Artifact base directory:
`smart-fuzzer/work/w109/G6-solvers/`. The W109 answer artifacts are working
evidence; the hashes above make the exact bytes referenced by this report
independently identifiable.

## Status axes and open lanes

- `execution_state: in_progress`
- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `open_lanes`:
  - identify the exact PMT annuity/expm1 intermediate over power-of-two and
    general rates;
  - distinguish observationally equivalent tau-formation graphs where their
    later precision lifetime matters;
  - identify the general-rate timing-factor operation order and store sites;
  - freeze and pass a prior-disjoint exact end-to-end PMT publication gate;
  - align production Rust, focused/full tests, contract rows, and the required
    Lean/formal route only after exact semantic identification;
  - reconcile the G6-01 catalog/map/worklist and bead state through the
    root-owned state lane;
  - retain alternate Excel application/channel, CPU, and workbook
    Compatibility Version sweeps as separate declared validation axes.

No FEC/F3E admission, coercion, type, shape, host, or evaluator-facing clause
was changed by this investigation. No OxFml handoff is opened by this record.
The XLL verification seam is not material to these scalar core/intermediate
black-box observations.

The independent EXT6 operation-tree search is not PMT evidence and is not used
to support any conclusion here. At report assembly,
`smart-fuzzer/work/w109/G6-solvers/optree_search3.log` records cleared
milestones only through shard `191/400`; its resumed run has not yet logged a
later cleared shard. The log is mutable while that search runs, so it is not
hashed or promoted as a finished result in this record.

## OPERATIONS Section 12 — Pre-Closure Verification Checklist

This is an explicit non-closure audit. Any `No` keeps G6-01 `in_progress`.

| # | check | result |
|---:|---|---|
| 1 | Function contract rows promoted for all in-scope PMT behavior | **No** — exact graph is unresolved. |
| 2 | Lean obligations satisfied/aligned | **No** — no exact route is available to align. |
| 3 | Rust implementation and required tests pass for identified semantics | **No** — no production change is claimed or authorized. |
| 4 | Deterministic replay per in-scope behavior | **No** for closure — deterministic investigative replays exist, but no exact end-to-end PMT replay exists. |
| 5 | Evidence links reproducible | **Yes** for this investigation — focused sources, artifact paths, hashes, provenance, and rerun scores are recorded. |
| 6 | Both version axes explicit | **No** for closure — build, bitness, and CV are explicit, but the distribution channel is not recorded; other application/CV axes remain open. |
| 7 | Public algebra versus empirical discrepancy resolved | **No** — the empirical operation graph remains unidentified. |
| 8 | XLL seam limitations recorded where material | **Yes** — the XLL seam is not material to these scalar observations. |
| 9 | Cross-repo impact assessed | **Yes** — no boundary or evaluator-facing clause changed, so no handoff is required. |
| 10 | No known semantic gap remains | **No** — the principal PMT graph gaps are listed above. |
| 11 | Completion-language audit passed | **Yes** — all claims are local investigative results and G6-01 remains open. |
| 12 | In-progress feature worklist updated | **No** in this one-file evidence task; root-owned reconciliation remains open. |
| 13 | Bead/blocker surface updated | **No** in this one-file evidence task; root-owned reconciliation remains open. |

Checklist result: `in_progress`; no completion claim is permitted.

## OPERATIONS Section 14 — Completion Claim Self-Audit

1. **Scope re-read: fail for closure.** The required current-reference PMT
   graph includes the hidden annuity intermediate and timing/publication order;
   neither is identified exactly.
2. **Gate criteria re-read: fail for closure.** The local metamer passes, but
   the general-rate frozen gate is only `378/480`, and there is no exact
   end-to-end frozen replay, production alignment, or formal-route alignment.
3. **Silent scope reduction check: pass for this investigation record.** The
   report explicitly limits the `832/832` claim to the power-of-two paired
   relationship, retracts the 100-pair and general-graph overclaims, and lists
   every known omitted lane.
4. **Looks-done-but-is-not check: pass.** Statistical association, negative
   racers, nuisance-parameter fitting, local metamers, and near-exact ULP scores
   are not presented as implementation or function closure.
5. **Result: fail for closure / retain `in_progress`.** G6-01 remains
   `scope_partial`, `target_partial`, and only partially integrated.
