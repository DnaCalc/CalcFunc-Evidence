# W109 G6-03 YIELD exact-graph research handoff — scope partial

Date: 2026-08-09

Function: `YIELD`

Workset lane: W109 G6-03
Reference baseline: Excel 16.0 build 20228, x64, workbook Compatibility Version 2

## Status

No exact discovery survivor was identified. The exact-graph lane therefore remains
research-only and scope partial. The frozen 288-row heldout stayed sealed and was
not opened, scored, or captured. No production source, shared documentation,
shared state, or bead was edited for this lane. `ODDFYIELD` was not started because
the prerequisite exact `YIELD` schedule was not found.

- `scope_completeness=scope_partial`
- `target_completeness=target_partial`
- `integration_completeness=partial`
- `execution_state=in_progress`

This report makes no implementation or closure claim.

## Clean-room provenance and capture contract

The work was strictly black-box and used only:

1. behavior observed through Excel's public worksheet interface;
2. public Microsoft `YIELD`/`PRICE` documentation;
3. the publicly published Apache-licensed ExcelFinancialFunctions root-finding
   family as a candidate reference, never as evidence of Excel internals; and
4. the OxFunc corrected `PRICE` forward kernel reconstructed from prior public-
   interface observations.

No Excel or Microsoft binary was disassembled, decompiled, dumped, or otherwise
inspected.

Every authorized capture used the following frozen contract:

- Excel 16.0 build 20228, x64;
- workbook Compatibility Version 2;
- typed binary64 argument cells through `Range.Value2`;
- relative `Formula2R1C1` evaluation through `cell_value2_bulk`;
- `NoCache`;
- exact validation of function name, call count, unique ordered witness IDs,
  ordered argument bit strings, and result kind;
- numeric results for every captured call;
- freshly observed Excel process count zero before launch and zero after bounded
  teardown; and
- explicit release of the serialized COM lane after capture.

The captures were serialized by the root campaign coordinator. This lane made no
ungranted COM launch and made no Excel call during the final offline races.

## Frozen evidence inventory and SHA-256

Paths below are relative to the OxFunc repository root. Hashes were verified on
2026-08-09 except for the two sealed heldout files: their values are the freeze-time
hashes and the files were deliberately not re-read during final handoff.

| Role | Path | SHA-256 |
|---|---|---|
| Historical 19-row input corpus | `smart-fuzzer/work/w109/G6-solvers/yield_corpus_out.json` | `86F9A228AC0B9F79E01492B219D48DD5CEC5B96FDCA580B04FE4FA102634C648` |
| Near-seed candidate manifest | `smart-fuzzer/work/w109/G6-solvers/candidate-manifest-yield-near-seed-v1.json` | `90287C2A82EABB25AB97DFA9A05E9005CA4F774450359C6E86FCE02DB7A3ADFA` |
| 384-row discovery metadata | `smart-fuzzer/work/w109/G6-solvers/meta-yield-near-seed-discovery-v1.json` | `3BE186B225FF45D6B38C5B9E300569D127F1E156F4BD502797C85043940C98E2` |
| 384-row discovery batch | `smart-fuzzer/work/w109/G6-solvers/batch-yield-near-seed-discovery-v1.json` | `EBE7D8728612F53B819C15A4050B937D87FF12CF6CDB6E949379908428919F76` |
| 384-row discovery answers | `smart-fuzzer/work/w109/G6-solvers/answers-yield-near-seed-discovery-20260809.json` | `7ECA7878533D35FF79F4C3A3BA199F43886AE553EF3CF64D8E86C8030FE315B2` |
| Sealed 288-row heldout metadata | `smart-fuzzer/work/w109/G6-solvers/meta-yield-near-seed-heldout-v1.json` | `33B6311D09C8DC08D9A7E62AC83CEAE653C31DC7412D1F8D53DB385D905D3B27` |
| Sealed 288-row heldout batch | `smart-fuzzer/work/w109/G6-solvers/batch-yield-near-seed-heldout-v1.json` | `528FB33A4E0AC6EE2E327AC7C27274F2971AB28C3594A023DBA65EABA8DD628A` |
| PRICE companion metadata | `smart-fuzzer/work/w109/G6-solvers/meta-price-yield-companion-discovery-v1.json` | `FAF52B156F5A10D1A19593F28AD104799F2ECF53D3850D4378B7AA0E3CA60A3C` |
| 136-row PRICE companion batch | `smart-fuzzer/work/w109/G6-solvers/batch-price-yield-companion-discovery-v1.json` | `A9A4E836239DE21C29A199A0F49A6C30EEAB3E48E606C0C816FEC615D6C07C1A` |
| 136-row PRICE companion answers | `smart-fuzzer/work/w109/G6-solvers/answers-price-yield-companion-discovery-20260809.json` | `2CFC211814251EA706D71CEF5B0B19FE1149FAEAEE4B0EEEE8F434F103DEB5D0` |
| 120-row seed-family metadata | `smart-fuzzer/work/w109/G6-solvers/meta-yield-seed-family-discovery-v2.json` | `8045A44DFA2E941AC09CFE8C4AD5F3E8A3506892E2A438447F9B475488D2F9A4` |
| 120-row seed-family batch | `smart-fuzzer/work/w109/G6-solvers/batch-yield-seed-family-discovery-v2.json` | `4E5F185AF01D350A9AD498402C3EF863C8D18608AA1571D6240BCEADFBD27597` |
| 120-row seed-family answers | `smart-fuzzer/work/w109/G6-solvers/answers-yield-seed-family-discovery-20260809.json` | `3E9C4230C32F8EB5A2E0E442C6DE97CAEAF010CC6B48F1BC0D6A6455D308AD5B` |
| Offline racer source | `smart-fuzzer/tools/calc_graph_racer/src/bin/race_yield_schedule.rs` | `A67928C0928362F7DDEFE751AB16FE3C10723ECAC60B9DED1CFC4B52C4F02D41` |

Freeze IDs:

- near-seed discovery/heldout/PRICE companion:
  `w109-g6-03-yield-near-seed-v1-20260809`;
- seed-family discovery:
  `w109-g6-03-yield-seed-family-v2-20260809`.

The report's own SHA-256 is supplied in the parent handoff rather than embedded
here, because embedding a file's digest in that same file is self-referential.

## Corrected PRICE forward-kernel evidence

The authorized PRICE companion contained 136 calls over the eight discovery
shapes at the seed and symmetric derivative probes. Current production
`price_kernel` replayed:

| Exact | Total | Maximum ULP | Sum ULP |
|---:|---:|---:|---:|
| 136 | 136 | 0 | 0 |

The racer's independently staged corrected local PRICE body also agreed with
`price_kernel` at all 1,152 sampled root-neighborhood evaluations. Platform
`powf`, a uniform x87 power chain, and repeated multiplication were separately
raced and did not improve `YIELD`. The corrected PRICE kernel is therefore the
controlled forward model used by these candidate races. It is not a completed
claim about Excel's exact `YIELD` objective, residual association, iteration
variable, or publication graph.

## Original frozen 384-row discovery

The discovery has eight disjoint shapes, 48 rows per shape. The expanded solver
VM evaluated 45,936 candidates over 29 seed kinds, numerical derivative direction
and step, convergence threshold, publication policy, and update association.

The best exact-count survivor remained:

- seed: `direct-gain_n-weight`;
- arithmetic: native binary64;
- derivative: central finite difference;
- absolute derivative step: `1e-6`;
- stop: `abs(dx) < 1e-10` (the tested `2^-33` threshold lands identically);
- publication: old/current iterate;
- cap: 100 iterations; and
- score: **58/384 exact, maximum 2,738 ULP, sum 147,012 ULP**.

All five tested update associations land on the same winning outputs for this
configuration.

| Discovery shape | Exact/48 | Maximum ULP | Sum ULP |
|---|---:|---:|---:|
| `d-oncoupon-short-b0-f2` | 15 | 2 | 41 |
| `d-offcoupon-short-b0-f2` | 1 | 64 | 1,237 |
| `d-oncoupon-long-b0-f2` | 36 | 75 | 86 |
| `d-offcoupon-b2-f2` | 2 | 92 | 1,522 |
| `d-offcoupon-b3-f2` | 0 | 111 | 2,606 |
| `d-oncoupon-b4-f1` | 0 | 341 | 14,691 |
| `d-offcoupon-b0-f4` | 0 | 2,738 | 125,847 |
| `d-leap-b1-f2` | 4 | 53 | 982 |
| **Aggregate** | **58/384** | **2,738** | **147,012** |

The frequency-4 off-coupon shape dominates the aggregate distance. At exact
corrected-PRICE roots, Excel often publishes a nearby retained iterate with a
small nonzero residual. For the quarterly center this displacement is about
1,200 ULP even though the corresponding Newton correction is already below
`1e-10`; therefore the start/path and publication graph materially affect the
answer bits.

## Seed-family fixed-point discovery

The second frozen discovery contains 120 calls over six nontrivial shapes. For
each available candidate-family fixed point it probes PRICE-target bit offsets
`-4`, `0`, and `+4` ULP. At the zero-offset centers, the encoded source seed is an
exact corrected-PRICE root and the local candidate solver publishes that root
exactly. Excel nevertheless publishes different bits for every source family.

The ten source families were:

1. `direct-gain_n-weight`;
2. `fractional-gain_n-weight`;
3. `fractional-gain_n-over-derived-off-squared`;
4. `fractional-gain_n-over-direct-off-squared`;
5. `fractional-gain_fractional-over-derived-off-squared`;
6. `direct-gain_direct-over-direct-off-squared`;
7. `direct-gain_n-over-direct-off`;
8. `direct-gain_n-plus-elapsed`;
9. `fractional-gain_textbook-average`; and
10. `direct-gain_n-weight_dirty-book`.

All available exact centers were refuted. The dirty-book family had no positive
fixed point on three shapes, which the frozen generator reports explicitly.

After expanding the solver VM to the same 45,936 candidates used above, the best
focused score was only:

- seed: `fractional-gain_n-over-direct-off-squared`;
- central absolute step `1e-9`;
- stop `abs(dx) < 1e-8`;
- publish new iterate; and
- **6/120 exact, maximum 1,229 ULP, sum 29,410 ULP**.

That focused leader does not generalize: on the original 384-row discovery it
does not beat the 58/384 baseline.

## Additional seed and solver families refuted offline

The expanded 29-kind seed surface included:

- all ten seed families in native arithmetic;
- all ten again with x87-style rounded seed arithmetic;
- fixed `0.0`, `0.05`, and `0.1`;
- coupon-rate and current-yield starts;
- multi-period extensions of the one-coupon closed form with derived and direct
  settlement offsets; and
- simple clean-price denominator approximations with fractional and direct
  remaining periods.

None improved the 58/384 exact count.

Further offline races refuted these broad families:

- forward, backward, and central finite differences;
- absolute steps `1e-3` through `1e-9` and raw-relative steps `1e-3` through
  `1e-7`;
- step thresholds `1e-7` through `1e-12` and binary thresholds `2^-30` through
  `2^-36`;
- old, new, and previous-iterate publication;
- five correction/update associations;
- analytic PRICE derivative, whose best exact count was 51/384;
- transformed period/weight families, whose best 52-exact result was 52/384,
  maximum 341 ULP, sum 49,819 ULP (`FractionalRemaining` with the
  `n/direct-off^2` weighting);
- native, x87, and mixed first-update spill graphs;
- alternate power paths; and
- fixed-iteration, secant, and false-position controls on the historical
  corpus. Bisection was used only to construct answer-blind fixed-point inputs
  for the focused v2 discovery, not as a historical-corpus YIELD solver race.

## Residual/objective graph race

The final objective race evaluated 95,040 candidates: 7,920 solver configurations
over five high-value seeds, crossed with twelve objective graphs.

| Objective graph | Best exact/384 | Maximum ULP | Sum ULP |
|---|---:|---:|---:|
| `PRICE - target` | 58 | 2,738 | 147,012 |
| `target - PRICE` | 58 | 2,738 | 147,012 |
| `(PRICE - target) / target` | 58 | 2,738 | 147,011 |
| `(target - PRICE) / target` | 58 | 2,738 | 147,011 |
| `PRICE / target - 1` | 43 | 2,809 | 153,304 |
| `1 - PRICE / target` | 43 | 2,809 | 153,304 |
| scaled difference, factor `0.01` | 45 | 2,704 | 146,718 |
| scaled difference, factor `100` | 45 | 2,707 | 146,843 |
| discounted dirty cashflows minus `(clean target + accrual)` | 58 | 2,738 | 147,012 |
| dirty-cashflow ratio minus one | 42 | 2,734 | 146,816 |
| Horner PV using `v^off`, `v=1/(1+y/f)` | 42 | 2,713 | 147,688 |
| Horner PV using `1/base^off` | 41 | 2,685 | 144,886 |

The dirty residual association therefore ties but does not distinguish the best
baseline. Both annual-y Horner graphs are refuted by exact count. A solver that
iterates the periodic rate or discount factor and only then publishes
`y = frequency * rate` remains graph-distinct and is not refuted by these annual-y
Horner rows.

## One-FD-bootstrap then secant race

The racer also evaluated 3,360 candidates that take one central finite-difference
Newton bootstrap step and then switch to secant updates. The cross product covered
four objective graphs, five seeds, native/x87 outer arithmetic, seven thresholds,
three publication policies, and four secant correction associations.

Best result:

- **30/384 exact**;
- maximum **1,618,118,678 ULP**;
- sum **70,395,977,187 ULP**; and
- normalized-difference objective, native arithmetic, direct-gain/n-weight seed,
  `1e-12` threshold, previous-iterate publication.

This family is materially worse than the finite-difference Newton baseline.

## Sealed heldout statement

The heldout batch contains 288 answer-blind calls over six shapes. It was frozen
before discovery answers were inspected. Because no exact 384-row discovery
survivor exists:

- the heldout batch was not opened during final analysis;
- no heldout Excel capture was requested or authorized;
- no heldout answer file exists for this lane;
- no heldout score was computed; and
- its batch and metadata hashes above are carried forward from freeze-time
  records, not a final re-read.

Opening or capturing this heldout requires a future exact discovery survivor and
a fresh explicit grant from the root campaign coordinator.

## Verification commands and observed results

Commands were run from
`smart-fuzzer/tools/calc_graph_racer` with an isolated target directory.

```powershell
$env:CARGO_TARGET_DIR='C:\Work\DnaCalc\OxFunc\target-yield-root'
cargo build --release --bin race_yield_schedule
```

Result: release build succeeded.

```powershell
cargo test --release --bin race_yield_schedule
```

Result: test harness succeeded; zero tests are defined in this standalone research
binary (`0 failed`).

```powershell
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' generate-seed-family-discovery
```

Result: both 120-row frozen artifacts were verified byte-identical; freeze ID,
six shapes, ten source families, and 120 calls were asserted.

```powershell
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' score-companion
```

Result: `PRICE companion production 136/136 max=0 sum=0`.

```powershell
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' race-original-seed-solver-vm
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' race-seed-family-solver-vm
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' race-objective-graphs
& 'C:\Work\DnaCalc\OxFunc\target-yield-root\release\race_yield_schedule.exe' race-fd-bootstrap-secant
```

Results: respectively 58/384, 6/120, 58/384, and 30/384 best exact counts,
with the detailed distance scores recorded above.

```powershell
Get-FileHash -Algorithm SHA256 <explicit frozen paths and racer source>
```

Result: hashes matched the inventory above. The sealed heldout paths were omitted
from the final hash command.

## Exact intentional path set

### Research tool and handoff authored by this lane

1. `smart-fuzzer/tools/calc_graph_racer/src/bin/race_yield_schedule.rs`
2. `smart-fuzzer/tools/calc_graph_racer/YIELD_EXACT_GRAPH_SCOPE_PARTIAL_20260809.md`

Both are intentionally untracked. Neither was staged or committed.

### Frozen lane evidence

1. `smart-fuzzer/work/w109/G6-solvers/candidate-manifest-yield-near-seed-v1.json`
2. `smart-fuzzer/work/w109/G6-solvers/meta-yield-near-seed-discovery-v1.json`
3. `smart-fuzzer/work/w109/G6-solvers/batch-yield-near-seed-discovery-v1.json`
4. `smart-fuzzer/work/w109/G6-solvers/answers-yield-near-seed-discovery-20260809.json`
5. `smart-fuzzer/work/w109/G6-solvers/meta-yield-near-seed-heldout-v1.json`
6. `smart-fuzzer/work/w109/G6-solvers/batch-yield-near-seed-heldout-v1.json`
7. `smart-fuzzer/work/w109/G6-solvers/meta-price-yield-companion-discovery-v1.json`
8. `smart-fuzzer/work/w109/G6-solvers/batch-price-yield-companion-discovery-v1.json`
9. `smart-fuzzer/work/w109/G6-solvers/answers-price-yield-companion-discovery-20260809.json`
10. `smart-fuzzer/work/w109/G6-solvers/meta-yield-seed-family-discovery-v2.json`
11. `smart-fuzzer/work/w109/G6-solvers/batch-yield-seed-family-discovery-v2.json`
12. `smart-fuzzer/work/w109/G6-solvers/answers-yield-seed-family-discovery-20260809.json`

The historical `yield_corpus_out.json` was read-only input. No file outside this
research/evidence set was intentionally changed by the YIELD lane.

## Diff discipline

The expected scoped status after this report is:

```text
?? smart-fuzzer/tools/calc_graph_racer/YIELD_EXACT_GRAPH_SCOPE_PARTIAL_20260809.md
?? smart-fuzzer/tools/calc_graph_racer/src/bin/race_yield_schedule.rs
```

There is no tracked diff under `smart-fuzzer/tools/calc_graph_racer` from this
lane. The shared worktree contains unrelated concurrent changes in production
files; they were preserved and not edited by this lane. No tracked diff was added
under `docs` or `.beads`.

## Open lanes

1. Identify the exact iteration variable: annual yield, periodic rate, or discount
   factor, including the final `frequency * periodic_rate` publication graph.
2. Identify any remaining corrected-forward residual/body association and exact
   retained-iterate arithmetic not represented by the raced objective graphs.
3. Produce one coherent candidate that is 384/384 exact on the frozen discovery.
4. Only then request authorization to capture and score the sealed 288-row
   heldout.
5. Only after an exact frozen heldout survivor, consider production code, focused
   Rust tests, shared evidence documentation, state, or beads.
6. Treat `ODDFYIELD` as a separate obligation: replay its odd-first forward
   objective before reusing any solver VM. A YIELD-only survivor cannot resolve
   the ODDFYIELD discrepancy.
7. Validate alternate Excel build/channel and workbook Compatibility Version axes
   in their own later phase.

## Completion-claim self-audit

- Exact discovery survivor: no.
- Heldout opened or scored: no.
- Production integration: no.
- Shared docs/state/beads edited: no.
- Partial work mislabeled as implementation or closure: no.
- Scope reduction hidden: no.

The required status remains `in_progress` / `scope_partial`.
