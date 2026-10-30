# ERF / GAUSS direct-tiny tied-graph disagreement checkpoint

Date: 2026-08-09

Parent commit: `6ae2293` (`W109 record ERF GAUSS route and store checkpoint`)

This is a discovery-only offline increment to
`ERF_GAUSS_ROUTE_STORE_OFFLINE_CHECKPOINT_20260809.md`. It does not alter a
production implementation, shared documentation, catalog, map, ledger,
BUG-FUNC-027, workset, bead, or other state surface.

## Evidence and provenance boundary

The replay reads exactly these existing GAUSS discovery pairs:

1. `batch-gauss-exact-discovery-v1.json` and
   `answers-gauss-exact-discovery-v1.json`.
2. `batch-gauss-route-discovery-v1.json` and
   `answers-gauss-route-discovery-v1.json`.

The loader fails closed on the answer provenance schema; Excel 16.0 build
20228, x64, Workbook Compatibility Version 2, `cell_value2_bulk`, and NoCache
with zero hits and misses; function name; exact bank counts; nonempty unique
IDs; scalar arity; numeric input and answer bits; duplicate input bits; and
batch/answer ID and argument parity.

No heldout path is named or read. The tool does not enumerate the G3-07
directory, read an ERF/ERFC answer, launch Excel or COM, or inspect a Microsoft
binary. Candidate arithmetic is limited to published TOMS 654 / CDFLIB
branch-190 and the project's public-semantics Ext80 research emulator.

## Existing-answer result

The parent race is reproduced exactly:

```text
graphs       11,520
rows          3,158
best exact    2,822/3,158
maximum ULP   1
sum ULP       336
aggregate ties 480
```

Full per-row output-vector comparison collapses all 480 tied graphs to one
behavioral class on the existing discovery rows:

```text
behavior classes       1
class multiplicity     480
disagreeing rows        0/3,158
greedy separator rows  0
```

Thus no ordering, signed residual, exactness mask, or answer-blind subset of
the already answered direct-route rows can choose among the 480 graphs. Their
aggregate tie is also a bit-for-bit per-row tie.

## Candidate-only disagreement result

The tool next constructs a deterministic answer-blind pool inside the proven
`abs(x) <= 1e-15` direct-route domain. It uses public IEEE-754 boundary
ladders, five mantissas per binary exponent, and an LCG with seed
`0x4733303754494553`; it removes existing discovery input bits. Neither row
selection nor ranking consults an expected answer.

```text
discovery-distinct pool inputs  30,032
candidate-disagreement inputs       14
behavior classes                      2
class multiplicities                 80 and 400
greedy separator inputs               1
```

The 14 disagreements are seven sign-mirrored pairs:

```text
0x02e64367549eb209  0x82e64367549eb209
0x04d4c6231fc300e4  0x84d4c6231fc300e4
0x050637ffcc5ed176  0x850637ffcc5ed176
0x08a57db8b14a5222  0x88a57db8b14a5222
0x0cb51ffb4e2d7c5f  0x8cb51ffb4e2d7c5f
0x0dd67b5b55e4d187  0x8dd67b5b55e4d187
0x1006380474b34294  0x9006380474b34294
```

The deterministic greedy separator is the first positive input:

| Input bits | Predicted bits | Graphs | Structural class |
|---|---|---:|---|
| `0x02e64367549eb209` | `0x02d1c37756a97d07` | 80 | `X87Continuous`, `WInnerThenG`, first product stored to binary64 |
| `0x02e64367549eb209` | `0x02d1c37756a97d08` | 400 | direct reuse of stored input `z` |

The other enumerated axes remain observational aliases inside these two
classes on this pool. In particular, the five exact-half placements retain
equal representation and do not create a distinct prediction class.

The canonical deferred discriminator payload is the 25-byte UTF-8 line
`GAUSS,0x02e64367549eb209` followed by LF. Its SHA256 is
`ADEE318EAC6B4284B1058F5C7051C76B97D166FCF4B041B35BBA6BC21B198230`.

This singleton is frozen only as answer-blind metadata in this report. No
probe batch, COM request, or answer file is created. The current 2,822/3,158
plateau is not an exact discovery survivor, so oracle execution remains gated.

## Deterministic replay

Run from the repository root:

```powershell
rustfmt --edition 2024 --check smart-fuzzer\tools\calc_graph_racer\src\bin\mine_erf_gauss_direct_tiny_ties.rs smart-fuzzer\tools\calc_graph_racer\src\bin\erf_gauss_tie_research\common.rs
cargo build --release --offline --locked --manifest-path smart-fuzzer\tools\calc_graph_racer\Cargo.toml --target-dir target-erf-gauss-tie-mining --bin mine_erf_gauss_direct_tiny_ties
.\target-erf-gauss-tie-mining\release\mine_erf_gauss_direct_tiny_ties.exe C:\Work\DnaCalc\OxFunc
```

Rustfmt and the offline release build pass. Capturing the executable stdout
through PowerShell `Out-String` produces 14 lines, 1,871 UTF-8 bytes, and
SHA256
`21BF4E013908EF6498644B52256105597E4B194B7C5FC369C8BA99B4E0A1889D`.

## Frozen hashes

```text
mine_erf_gauss_direct_tiny_ties.rs
  1191DCF1E3414839E69815EA2A64CA1CF5CCBBAABABC00F414CE03CED8A0D9A3
erf_gauss_tie_research/common.rs
  3049E37155C920F55225EEAE174E288396F2F387D52281BE0A6BC4444C362BD1
audit_erf_gauss_route_store.rs
  374C095A524B9B51502520D94F81D1F1F55D7A96B8964954176B0D939DF1066F
ERF_GAUSS_ROUTE_STORE_OFFLINE_CHECKPOINT_20260809.md
  CB51E277CDE859EFC63D14A28090F5717B5666FC792EA076E97CF20BD045E7D3
batch-gauss-exact-discovery-v1.json
  8627F7E248545CB618684EFA24D76336BBE9C6A545B7BCFE2CE2D9CE3F3395A3
answers-gauss-exact-discovery-v1.json
  8BFFAF353EFFDB54F15B82CCA4997E35761E4F65A51A0991B169C1CA75AFBCA8
batch-gauss-route-discovery-v1.json
  28F0BEBFBF5354A5624DAC7B0C6A27EF01E74ADD10E85DF513C0DC51E6EE4F93
answers-gauss-route-discovery-v1.json
  2D225BDB490FC8B6EF980B68B5993ACE4E69F97262D60885F4C7CBDF9E1FD1B1
```

## Gate and status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`

`open_lanes`:

1. Resolve the common 336 one-ULP residuals with one coherent public graph.
2. Identify the x87-recovery versus stored-`z` route without executing the
   deferred discriminator before the exact-survivor gate.
3. Separate or prove semantic aliasing for the remaining graphs inside the
   80- and 400-member prediction classes.
4. Resolve the broader ERF/ERFC body, tail, and boundary graphs.
5. Execute frozen heldouts only after a coherent exact discovery survivor and
   explicit serialized root authorization.
6. Production, tests, formal model, shared state, catalog, and ledger work
   remain outside this increment.
