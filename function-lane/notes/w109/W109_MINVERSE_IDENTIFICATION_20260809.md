# W109 MINVERSE Current-Reference Calculation-Graph Identification

Status: `closed_signed_off`

Scope: OxFunc-owned `MINVERSE` numeric-array semantics on Excel 16.0 build
20228 x64, workbook Compatibility Version 2. The downstream final-cell
publication of a `1x1` array is excluded and remains under `CSC-0024` /
`HO-FN-010`.

## 1. Result

Excel uses the already-identified right-looking Doolittle LU decomposition
with partial pivoting and per-column unit-vector solves. The missing graph axis
was arithmetic publication: every one of these eight sites is
`RN53(RN64(op))` rather than an ordinary binary64 operation:

1. LU factor division;
2. elimination multiply;
3. elimination subtract;
4. forward-solve multiply;
5. forward-solve subtract;
6. backward-solve multiply;
7. backward-solve subtract;
8. final back-substitution division.

After the solve, every numeric zero result is published as positive zero. No
intermediate is retained continuously across multiple operations in x87.

The identified implementation landed in `bce3558`. It changes no function
admission, coercion, FEC/F3E, evaluator-facing clause, or array-result shape.

## 2. Why The July Conclusion Was Wrong

The July experiment correctly ruled out a continuously retained x87 body, but
incorrectly generalized that negative result to “plain SSE2 double.” Its 16
models used broad register-retention/store regions and never enumerated the
legacy per-operation pattern `RN53(RN64(op))` independently at all sites.

The new scorer exhausts all `2^8 = 256` per-site masks. On the original `607`
cells, every mask with the final-divide bit set collapsed at `607/607`, so that
corpus could identify only the final divide. A targeted answer-blind battery
was therefore necessary.

## 3. Discovery, Refinement, And Publication Gates

### 3.1 Banked evidence

The three existing answer sets contain `607` cells. Plain Doolittle scored
`598/607`; mask `0x80` and every lower-bit observational equivalent scored
`607/607`.

### 3.2 Retired refinement set

The first deterministic generator excluded all banked matrices and produced
`576` rows:

- `256` plain-versus-final-divide disagreements;
- `32` candidate-versus-extra-x87 disagreements for each of the other seven
  arithmetic sites;
- `96` collapse controls.

Live answers selected all eight x87 sites, not the provisional final-divide-
only graph. They also exposed five `-0` versus Excel `+0` publications. Because
these answers changed the model, this entire set is explicitly retired into
refinement. With the corrected full-x87 plus positive-zero graph it is
`576/576`.

### 3.3 Frozen disjoint publication gate

The second generator excluded every banked and refinement matrix before any
new answer was obtained. It produced `416` rows:

- `32` disagreements for each of the eight single-missing-x87-site models;
- `64` signed-zero publication rows;
- `96` collapse controls.

Fresh matrix `Range.Value2` / `INDEX(MINVERSE(...),r,c)` NoCache capture began
and ended with zero Excel processes. Embedded provenance records Excel 16.0
build 20228, 64-bit, workbook Compatibility Version 2, Windows x64, matrix
Value2 plumbing, runner v2, and PowerShell 7.6.3.

The frozen graph scored `416/416` and is the unique 256-mask survivor. Every
single-missing-site model lost its 32 targeted rows. Plain and final-divide-
only controls scored `160/416` and `192/416` respectively.

## 4. Durable Evidence

All generated artifacts are under
`smart-fuzzer/work/w109/G5-01-minverse/` and are gitignored evidence regenerated
by the committed generator.

| Artifact | SHA-256 |
| --- | --- |
| `G5-01-answers-minverse.json` | `B84C867AC5B9DA701BFB7E320E6670D05D2675BD72C0CDEFA39286E0E649809B` |
| `G5-01-answers-minverse-r1.json` | `5A7D75012B9C64A3F406DF0C5114D93691DD66DA5436CDC749BC6699650EF2AA` |
| `G5-01-answers-m4b.json` | `DEED368EA23EF6ED1B10D773BD31606FEE4A0481325492AD66F801EB983828B5` |
| refinement batch | `8E22395B0F56E430AAF3249533A22C7358FCFC48A2433C7F62DAB0D788518F7E` |
| refinement meta | `BCD85503DB214A13169258F1EB70A428A5BBF3986076FCA91FC58EAB6BEBA5F5` |
| refinement manifest | `CC16E197135311BACDBE1B4B368380A504018F1FAB642D338FAF8769763E315E` |
| refinement answers | `65BD93C9D7D54F34B2B6D5A15A38770920BBCA934DE6D7123371A5DFA393D34B` |
| publication batch | `2D27FBDC9B27D3DBC1311C125D49017C67DAED348C9551B199A13621EB367375` |
| publication meta | `E86B55E3D832C7971C61340F3C4220C5911409F79DB980DB0A045099E38B2F91` |
| publication manifest | `67CD7BF5758FF878AA61911A186E357770A1F1C3A4013641B4430A463A3FC7DA` |
| publication answers | `6564878727E68DCE3E18655288245EBCE1BC161D3684E519F4C442C92BCAA4EE` |
| generator source | `D074D5D40E249176C315B6B93BDD2EEA15F96A2F652F2347FD27B252D711AE7F` |
| scorer source | `13B9CF5B38B3035D299A22DB25E08C043B87C724F5BBFE0DCF48CEEAC5647FFE` |

The direct compiled-production replay is `607/607 + 576/576 + 416/416 =
1599/1599`.

## 5. Implementation And Validation

1. Production uses `excel_x87_div`, `excel_x87_mul`, and `excel_x87_sub` at
   the eight identified sites and normalizes only completed output zero cells.
2. Nine exact unit pins cover one discriminator per arithmetic site plus the
   independent positive-zero rule.
3. `race_minverse_residual` validates batch/answer IDs, exact matrix argument
   bits, result indices, NoCache mode, Excel build/bitness/CV, and matrix
   plumbing before scoring.
4. Focused exact-pin test: `1/1` passed.
5. Full `oxfunc_core`: `1521` passed, `4` ignored; all integrations and
   doctests passed.
6. Lean `MatrixFamily` records the eight-site route and positive-zero binding
   without duplicating the x87 numeric engine; full Lean build passes `492`
   jobs.

## 6. OPERATIONS Section 12 — Pre-Closure Verification

| # | Check | Result |
| ---: | --- | --- |
| 1 | Function contract rows complete and promoted? | yes — matrix contract and FDEF-069 aligned |
| 2 | Lean obligations satisfied/aligned? | yes — executable route binding; 492-job build |
| 3 | Rust implementation and tests pass? | yes — focused and full core green |
| 4 | Deterministic replay artifact exists? | yes — committed generator/scorer plus three evidence tiers |
| 5 | Evidence links reproducible? | yes — exact paths, hashes, IDs, args, and provenance validated |
| 6 | Both version axes explicit? | yes — Excel 16.0 build 20228 x64 and CV2 |
| 7 | Public-doc/empirical discrepancy handled? | yes — empirical per-operation x87 graph is authoritative |
| 8 | XLL seam limits documented where material? | yes — `1x1` final-cell publication remains HO-FN-010; numeric kernel is local |
| 9 | Cross-repo impact assessed/handoff filed if needed? | yes — no new seam change; no new handoff required |
| 10 | No known semantic gap remains in declared scope? | yes |
| 11 | Completion-language audit passed? | yes — closure is limited to current-reference MINVERSE numeric semantics |
| 12 | In-progress worklist updated? | yes — MINVERSE removed from W109 open lanes |
| 13 | Bead/blocker surface updated? | yes — `oxf-dzfk` closed with evidence; parent seam bead remains open |

## 7. OPERATIONS Section 14 — Completion Claim Self-Audit

1. **Scope re-read — pass.** Exercised numeric-array semantics match the
   declared slice; `1x1` final-cell publication is explicitly excluded.
2. **Gate criteria re-read — pass.** Discovery, retired refinement, fresh
   disjoint publication, production replay, exact pins, full core, contract,
   Lean, state, and bead gates pass.
3. **Silent scope reduction — pass.** No numeric dimension, matrix family, or
   arithmetic site was removed; the pre-existing downstream publication seam
   is named explicitly.
4. **Looks-done-but-is-not patterns — pass.** No stubs, tolerance comparisons,
   nudges, answer-selected publication rows, unexercised contract text, or
   unacknowledged new handoff is used.
5. **Result included — pass.** This section and the three-axis result below are
   the scoped completion record.

## 8. Three-Axis Result

For current-reference `MINVERSE` numeric-array semantics:

1. `scope_completeness`: `scope_complete`
2. `target_completeness`: `target_complete`
3. `integration_completeness`: `integrated`
4. `open_lanes`: `[]`

The wider W109 campaign remains `scope_partial` / `target_partial` / `partial`.
Its open lanes include PMT-family, CONVERT, COMBIN, GAMMA/GAMMALN,
distribution/regression rows, the remaining catalog, broad post-catalog
discovery, and alternate application/channel/Compatibility-Version axes.
