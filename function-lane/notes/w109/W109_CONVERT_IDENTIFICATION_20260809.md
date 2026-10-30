# W109 CONVERT Current-Reference Calculation-Graph Identification

Status: `closed_signed_off` for the current-reference CONVERT G4-05 slice

Implementation, formal binding, evidence tooling, and exact pins landed in
commit `8ef5cac`.

Scope: OxFunc-owned `CONVERT` semantics for the declared unit catalog on Excel
16.0 build 20228 x64, workbook Compatibility Version 2. Locale, alternate
Excel-version/channel, and alternate-architecture realization are orthogonal
future phases.

## 1. Result

The current reference uses a generic three-store graph for every supported
linear category. Each arithmetic operation is evaluated under x87 PC64 and
stored to binary64 before the next operation:

1. `product = RN53(RN64(number * from_factor))`;
2. `core = RN53(RN64(product / to_factor))`;
3. `result = RN53(RN64(core * decimal_prefix_delta))`.

The prefix delta is one correctly rounded binary64 representation of decimal
`10^(from_prefix_exponent-to_prefix_exponent)`. It is not formed by dividing
two prefix factors or folded into either direct-unit factor.

The identified tables and dispatch rules are:

1. length uses exact integer angstroms per direct unit;
2. mass, time, and volume use their direct physical binary64 constants;
3. pressure stores independently rounded reciprocals of the public
   units-per-pascal entries; `bar` is unsupported and returns `#N/A`;
4. temperature uses six direct binary64 affine pair formulas plus identity
   passthrough, not universal composition through Kelvin;
5. unsupported units and cross-category pairs return `#N/A`.

This changes no admission, coercion, FEC/F3E, evaluator-facing clause, or
result shape. No cross-repo handoff is required.

## 2. Discovery And Retired Gates

### 2.1 Discovery bank

The clean typed NoCache discovery bank contains `7,026` rows across length,
mass, time, pressure, volume, and temperature. The final graph is
`7,026/7,026`.

### 2.2 Retired v1 publication attempt

The first frozen candidate missed `12/5,586` rows. After those answers were
used for model refinement, the set was explicitly retired. The final graph is
`5,586/5,586` on it.

### 2.3 Retired v2 publication attempt

The second candidate missed one row:

`CONVERT(f64::from_bits(0x457bc2d00cc56eb2), "nm", "Pm")`

It predicted `0x4080c7cdff92ed2f`; Excel returned
`0x4080c7cdff92ed2e`. The entire `6,915`-row set was explicitly retired before
using that answer. The final graph is `6,915/6,915` on it.

### 2.4 Value2/readback control

An independent `18`-row capture read the argument cell, a direct reference,
`CONVERT` output, and base-meter identity output through `Range.Value2`. The
requested input bits survived unchanged. Around the v2-kill mantissa, the
identity mapping exposed the missing first-product store. The final graph is
`18/18`.

## 3. Refinement And Frozen Publication

### 3.1 Refinement-only v3 discriminator

A typed `4,226`-row length battery replayed the kill mantissa across direct
pairs and prefix directions, adjacent values, and power boundaries. It was
declared refinement-only before capture. The expanded schedule search found
the three-store graph at `9,408/9,408` length rows and `18/18` readback rows;
the final unified graph is `4,226/4,226` on the refinement battery.

### 3.2 Frozen disjoint v3 publication gate

The v3 generator excluded all `23,558` prior unique tuples before reading any
new oracle answer. Deterministic regeneration reproduced the same batch,
metadata, and synthetic-answer hashes. The `10,418` rows contain:

1. `4,872` two-pass ordered all-pair rows, covering forward and reverse
   orientation and every supported prefix;
2. `4,922` signed neighbors on a broad power-of-two ladder for every direct
   ordered pair;
3. `96` first-product PC64-store discriminators;
4. `96` quotient PC64-store discriminators;
5. `432` independent temperature rows.

Fresh NoCache capture began and ended with zero Excel processes. Provenance
records Excel 16.0 build 20228, 64-bit, workbook Compatibility Version 2,
Windows x64, typed `cell_value2_bulk` input plumbing, bulk `Range.Value2`
result readback, and runner v2.

The frozen graph scored `10,418/10,418`, with even and odd partitions each
`5,209/5,209`, maximum ULP error `0`, and sum ULP error `0`. All six categories
are exact. The held-out also selects both generic store axes independently:

| Candidate | Overall | First-store rows | Quotient-store rows |
| --- | ---: | ---: | ---: |
| frozen generic three-store graph | 10,418/10,418 | 96/96 | 96/96 |
| retired native-f64 core | 10,226/10,418 | 0/96 | 0/96 |
| global first store, native quotient | 10,322/10,418 | 96/96 | 0/96 |
| length-only first store | 10,250/10,418 | 24/96 | 0/96 |
| length-only first and quotient stores | 10,274/10,418 | 24/96 | 24/96 |

No publication answer was used to change the graph, scorer, generator, batch,
metadata, or table constants.

## 4. Durable Evidence

Generated evidence is under `smart-fuzzer/work/w109/G4-convert/` and is
gitignored; committed generators, scorers, exact pins, and this hash ledger
make it reproducible.

| Artifact | SHA-256 |
| --- | --- |
| clean discovery answers | `F626A193C9D096A1FA95D5A6B5E64B2FCA6C96D856D3DE080D1E2174212031E7` |
| retired v1 answers | `EC6EC246B90D16CCF61EA7EF0C922F2D31EE7E220F963424202E708E749FB684` |
| retired v2 batch | `122643B7A9ABE955402DC82FD704583A4C2218C1AF355888E95D053C64B553DC` |
| retired v2 metadata | `0BC3EE0623465708EFAF5D03ED1E7EA1C1017C14C7C5FC280A53C57FEEF21D63` |
| retired v2 answers | `BB4A32495A3A67AC54DD91E2D66BE4C68AF0BD1E10C4D2600B31218AD680C404` |
| v3 refinement batch | `1D78288385E9F4FEFD10C3537A5F02225B794B9F8E88A23CE6E40C9280C8D225` |
| v3 refinement metadata | `8313246D19D40A8E3012A0C0654142FD8630023A556C4A86FE1316457590A6A1` |
| v3 refinement answers | `A3A2854997A38555E7277620875D33E27312ABA3E35162EB3D133370633E9763` |
| v3 publication batch | `0F56D512F849341D6DA7710F747586527D457D3AA1BF15FACAB6C62FFA5F481B` |
| v3 publication metadata | `80D5343027528D0B778E0D7AFFF802C40C05F32D05A63934AB20ADAC1AC60AC9` |
| v3 publication answers | `CA813A2F2AEB8F6B5A7FDF1E19B741D205E0074BEA769E5B500B5E57433BF87F` |
| v3 publication score | `EA9C0145BAEF73E95BEA040BEA0216F6DA5F85C53D063E291231A948FDA27740` |
| v3 freeze record | `2932F6BF0A1CCE2601D67C8EF78CCEB2F7067F1A2B2D7A9AFDAAC3CFD2A1CBB3` |
| v3 result record | `A75CDE7B42C4EC8FB3FA8F8B643B882CFC681800629EBA92CFB74AD57D3FEEBB` |
| frozen model source | `40707690B6D1424155842DCDAE703AA043938934EB9AFD69244E608B6A33E6EE` |
| frozen scorer source | `6930B69FF32828EFF4C523658419ED2A6CDC478460132D38427B5D11A1A4D19D` |
| frozen generator source | `2C6739802F3D0A492FB502EBF844B3B34DC4DDAA3FCFD9181615895141503C6A` |
| production replay source | `6C92E6B9C003FD1EA87B834CA959F9D2DE5F5532D402996EC1050AC54EA0F977` |
| production replay score | `141341187BB29DBB6F4F93A6ABCD25D1C8CD6826771B86DDAC399238B36AA479` |

## 5. Implementation And Validation

1. `convert_kernel` uses existing `excel_x87_mul` / `excel_x87_div` helpers at
   all three identified sites and keeps direct factors separate from prefix
   exponents.
2. Thirteen exact numeric pins span discovery, both retired sets, refinement,
   every discriminated publication category/site, and time-prefix coverage.
3. Separate exact pins cover the direct temperature route and `bar => #N/A`
   in both directions.
4. `replay_convert_production_v3` validates answer IDs, exact typed arguments,
   NoCache mode, Excel build/bitness/CV, and Value2 plumbing before calling the
   compiled production kernel.
5. Direct production replay is `34,189/34,189`:
   - discovery `7,026/7,026`;
   - retired v1 `5,586/5,586`;
   - retired v2 `6,915/6,915`;
   - refinement `4,226/4,226`;
   - publication `10,418/10,418`;
   - Value2/readback control `18/18`.
6. Mixed scalar helper tests pass `39/39`, OracleCache helpers pass `38/38`,
   and the scheduler loop smoke is green.
7. Full `oxfunc_core` passes `1,527` tests with `4` ignored; all integration
   tests and doctests pass.
8. Lean `MiscConversionFamily` records the three stored sites, table/prefix/bar
   policy, direct temperature routes, and rational value ordering without
   duplicating x87 arithmetic; full Lean build passes `492` jobs.

## 6. OPERATIONS Section 12 — Pre-Closure Verification

| # | Check | Result |
| ---: | --- | --- |
| 1 | Function contract rows complete and promoted? | yes — the conversion contract and FDEF-056 are aligned to the exact current-reference route |
| 2 | Lean obligations satisfied/aligned? | yes — executable route binding and 492-job build |
| 3 | Rust implementation and tests pass? | yes — focused pins, full core, integrations, and doctests green |
| 4 | Deterministic replay artifact exists? | yes — committed generator/scorer/replay sources plus five evidence tiers |
| 5 | Evidence links reproducible? | yes — exact paths, hashes, IDs, arguments, and provenance validated |
| 6 | Both version axes explicit? | yes — Excel 16.0 build 20228 x64 and CV2 |
| 7 | Public-doc/empirical discrepancy handled? | yes — empirical `bar => #N/A` and operation graph are authoritative |
| 8 | XLL seam limits documented where material? | yes — no material XLL qualification for the pure scalar kernel; live worksheet Value2 is authoritative |
| 9 | Cross-repo impact assessed/handoff filed if needed? | yes — no FEC/F3E or evaluator-facing change, so no handoff is required |
| 10 | No known semantic gap remains in declared scope? | yes |
| 11 | Completion-language audit passed? | yes — only the declared current-reference CONVERT slice is signed off; wider W109 stays partial |
| 12 | In-progress worklist updated? | yes — catalog, map, workset register, W109 owner, and worklist are synchronized |
| 13 | Bead/blocker surface updated? | yes — `oxf-jwh5.8` is closed signed off while the W109 epic remains in progress |

## 7. OPERATIONS Section 14 — Completion Claim Self-Audit

1. **Scope re-read — pass.** The exercised current-reference unit catalog,
   prefixes, table construction, store graph, temperature routes, and error
   dispatch match the declared slice.
2. **Gate criteria re-read — pass.** Discovery, retired refinement,
   disjoint publication, production replay, exact pins, full core, contract,
   Lean, and shared-state reconciliation gates pass.
3. **Silent scope reduction — pass.** No supported category, ordered pair,
   prefix, sign, power ladder, temperature pair, or `bar` error lane was
   removed.
4. **Looks-done-but-is-not patterns — pass.** There are no tolerance-based
   parity claims, numeric nudges, answer-selected publication rows, stubs, or
   unexercised contract/formal additions.
5. **Result included — pass.** The three-axis status below records the scoped
   integrated result while keeping the wider campaign explicitly partial.

## 8. Three-Axis Result

For the declared current-reference `CONVERT` semantic slice:

1. `scope_completeness`: `scope_complete`
2. `target_completeness`: `target_complete`
3. `integration_completeness`: `integrated`
4. `open_lanes`: `[]` within G4-05. Locale, alternate Excel
   version/channel, and alternate architecture are orthogonal future phases
   outside this current-reference slice.

The wider W109 campaign remains `scope_partial` / `target_partial` / `partial`.
