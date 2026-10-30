# W109 IRR Exact-Graph Discovery Checkpoint — 2026-08-09

Status: `in_progress`

- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`
- `open_lanes`:
  1. identify an exact IRR objective graph on the frozen 300-row discovery set;
  2. identify the remaining solver schedule/publication bits after the objective is exact;
  3. freeze one exact discovery survivor before opening the 180-row heldout answers;
  4. validate the frozen survivor on heldout and adversarial rows;
  5. only then consider production, test, and formal alignment.

This checkpoint preserves the W109 `G6-06` IRR clean-room discovery state at
the timebox boundary. It is not a function-phase claim and makes no production
or integration claim.

## 1. Scope and guardrails

The lane used only:

1. public documentation and public source candidates;
2. reproducible black-box Excel behavior through worksheet formulas and
   `Range.Value2`;
3. offline calculation-graph enumeration.

No Excel or Microsoft binary was disassembled, decompiled, dumped, or otherwise
inspected. The public candidate source used for the `LDoNPV` and `OptPV2`
statement graphs was Microsoft's published
[`Financial.vb` Reference Source](https://github.com/microsoft/referencesource/blob/main/Microsoft.VisualBasic/runtime/msvbalib/Financial.vb).
Those public graphs were treated as candidate shapes, not as evidence about
Excel internals.

No catalog, function-status map, workset, workset register, bead, production,
test, or formal file was edited. Nothing was staged or committed.

## 2. Frozen discovery and sealed heldout

### Original IRR discovery

| Artifact | Rows / bytes | SHA-256 |
|---|---:|---|
| `smart-fuzzer/work/w109/G6-solvers/batch-irr-exact-graph-discovery-20260809.json` | 300 / 51,260 | `93E340A1A571799519DA9D38B26996C8BBA439B7BF646C9185D3966874B55A98` |
| `smart-fuzzer/work/w109/G6-solvers/meta-irr-exact-graph-discovery-20260809.csv` | 300 / 55,156 | `F7BC8172F6AEAF6C759059FD0A524A4315160D7818B3FE275504B8ED1A5BDCE2` |
| `smart-fuzzer/work/w109/G6-solvers/answers-irr-exact-graph-discovery-20260809.json` | 300 / 99,284 | `ED101AE3304C93C51C99034F721C3E1BBA79B8A1A99DB3346BC48D5E8EFBFBAA` |

The discovery answers contain 270 numeric results and 30 `#NUM!` results. The
30-error boundary is exactly all 15 `d11` huge-scale rows plus all 15 `d14`
power-of-two-large rows.

### Heldout seal

| Artifact | Rows / bytes | SHA-256 |
|---|---:|---|
| `smart-fuzzer/work/w109/G6-solvers/batch-irr-exact-graph-heldout-20260809.json` | 180 / 33,070 | `5CAACBFCFEA62B8633C27E1A31A5369B206F879C0BA95064262561ACAEBD074C` |
| `smart-fuzzer/work/w109/G6-solvers/meta-irr-exact-graph-heldout-20260809.csv` | 180 / 35,055 | `E3BA940A4575875CEB74E0548331982CD01289CB9B214283E9DA6D0AE81B8F70` |

The heldout answer artifact does not exist. No heldout answer was captured or
read during this lane. The heldout remains sealed because discovery has no exact
survivor.

## 3. Discovery-only worksheet-NPV companion

The companion derives three answer-blind evaluation points from every frozen
IRR discovery input:

1. `base`: the exact source guess bits;
2. `v_h_neg`: `v = 1/(1+guess)`, then `v - binary32(0.001)` widened exactly to
   binary64, then `rate = 1/v - 1`;
3. `v_h_pos`: the corresponding positive perturbation.

Each of the 900 points captures three separate worksheet surfaces:

1. raw `NPV(rate,c1..cn)`;
2. direct `NPV(rate,c1..cn)+c0` in one formula;
3. `raw_npv_cell+c0` in a separate formula.

| Artifact | Rows / bytes | SHA-256 |
|---|---:|---|
| `smart-fuzzer/work/w109/G6-solvers/batch-irr-npv-objective-companion-discovery-20260809.json` | 900 / 413,825 | `C114745B446EE166BFD927904BD5158143B52267CB844D8A906275201B7CAA9F` |
| `smart-fuzzer/work/w109/G6-solvers/meta-irr-npv-objective-companion-discovery-20260809.csv` | 900 / 233,741 | `E4542AD49581B80E23D5EFA6A9464F271922735852C10EFCA8E45AA0CFBD8E45` |
| `smart-fuzzer/work/w109/G6-solvers/answers-irr-npv-objective-companion-discovery-20260809.json` | 900 / 1,123,965 | `C421FC537E289AF4E57B6049677E950B4934516A5E0ABA001B4083C027527B18` |

### Capture provenance

- Excel version: `16.0`
- Excel build: `20228`
- bitness: `64-bit`
- Workbook Compatibility Version: `2`
- cache: `no_cache`
- input plumbing: one exact binary64 `Range.Value2` matrix with immediate
  bit-for-bit readback, followed only by `Formula2R1C1` cell references
- calculation calls: one
- source alignment: 300 unique source IDs, three points per source, all
  `c0`/tail/guess bits and all derived `v0`/`h`/evaluation-`v`/rate bits
  independently replayed before Excel launch
- result kinds: 900 numeric raw NPV, 900 numeric direct-composed, and 900
  numeric cell-composed results
- Excel process count: `0` before and `0` after
- runner: `smart-fuzzer/tools/Run-W109IrrNpvObjectiveCompanion.ps1`, 25,108
  bytes, SHA-256
  `5A1E23BD0EA93002A87E8D461BA2BE4A92FAA8DA59D283B604458C3CE7D5E184`

The first authorized launch stopped before formula entry because the custom
PowerShell range helper allowed COM-range enumeration. Its bounded teardown
returned Excel to process count zero and wrote no output. The only runner change
was the scalar-return guard `return ,$Worksheet.Range(...)`. An offline
enumerable-range contract check then proved that the helper returned the range
object with its `Value2` property rather than its children. A fresh serialized
authorization was obtained for the rehashed runner above; that capture produced
the answer artifact and returned to process count zero.

## 4. Objective-boundary findings

### 4.1 The worksheet evaluator has a cancellation-to-zero correction

The two composed surfaces are bit-identical on all 900 rows:

```text
direct NPV(...)+c0 == raw_npv_cell+c0    900/900
```

Recomposing from the published raw `Value2` bits with strict binary64, PC64
x87/store, or PC53 x87/store addition matches only `882/900`. The 18 mismatches
are all base-point near-exact cancellations: strict addition yields a nonzero
residual, while Excel publishes positive zero.

The observed scale-relative boundary is:

```text
largest snapped |raw+c0| / max(|raw|,|c0|) = 5.684341886080802e-16
smallest published-nonzero ratio             = 2.830802259268159e-14
```

On this discovery set, every threshold from `3 * 2^-52` through `64 * 2^-52`
classifies all 900 rows identically. The exact threshold constant is therefore
not identified. A 15-significant-digit decimal-equality hypothesis scores
`899/900`; the scale-relative binary bracket is the stronger current model.

This is not exact compensated addition: the exact sum of the two published
binary64 operands is nonzero on those 18 rows. It is not a solver-only residual
snap: the same zero occurs in standalone worksheet formulas and through a raw
NPV result-cell reference.

### 4.2 IRR does not inherit that evaluator snap

Joining the 18 nontrivial worksheet-snap base rows to the frozen IRR discovery
answers gives:

- 16 numeric IRR rows, all 16 different from the supplied guess;
- two IRR `#NUM!` rows (`d11` and `d14`);
- zero IRR guess-passthrough rows.

The guaranteed 72-row two-step subset contains two particularly decisive rows,
`d16-m28` and `d16-p28`: the worksheet-composed objective is zero, but Excel IRR
does not return the guess. Therefore worksheet-evaluator snapping and the
internal IRR objective must remain separate claims.

Applying the smallest exact-classifying snap rule to the reverse worksheet-NPV
candidate harms the frozen 72-row score:

| Candidate | Exact | ULP sum | Max ULP |
|---|---:|---:|---:|
| reverse worksheet-tail composition, no snap | 40/72 | 4,280 | 1,024 |
| same graph plus evaluator snap | 37/72 | 536,875,404 | 306,276,560 |

## 5. Offline graph-race findings

### 5.1 Raw worksheet NPV

The current raw-NPV leader is reverse-Horner division. Over the new companion:

```text
exact       636/900
by point    base 229/300, v_h_neg 199/300, v_h_pos 208/300
ULP sum     342
max ULP     4
```

The leading staging stores `w = 1+rate` and each reverse-Horner numerator, while
the division remains resident until the next numerator. Reverse algebra shifts,
seed-first variants, and reciprocal variants tie and do not remove the residue.
The documented public `Microsoft.VisualBasic.Financial.NPV` API scores 485/900
on this corpus. No raw worksheet-NPV candidate is exact.

### 5.2 IRR guaranteed two-step subset

The frozen answer-blind local subset is the four `m28`, `p28`, `m34`, and `p34`
rows for each of the 18 numeric shapes: 72 rows total. Curvature across the
degree-wide shapes independently identifies an unscaled objective in
discount-factor space and an absolute step near `0.001`; the `v*f` and `f/v`
objective scalings are shape-inconsistent.

The current no-snap leader is:

```text
objective graph  ForwardAddProductWorksheetNpvMulW
objective mask   560 (bits 4, 5, 9)
w graph          ReciprocalV
h                negative binary32(0.001), widened to binary64
update           CrossProducts
schedule mask    448 (stored cross numerator, updated v, publication reciprocal)
publication      1/v - 1
exact            44/72
ULP sum          5,476
max ULP          1,024
```

This improves the earlier 43/72 discovery leader by one row but is still
partial. No answer-driven row patch was introduced, and no candidate is eligible
for heldout use.

The public `Microsoft.VisualBasic.Financial.IRR` API is also not a substitute:
it scores only 2/300 exact against this Excel discovery battery and does not
reproduce Excel's 30-row `#NUM!` boundary.

## 6. Replay

All paths below are relative to
`smart-fuzzer/tools/calc_graph_racer` unless stated otherwise.

### Generate and validate the answer-blind companion

```powershell
cargo run --quiet --bin generate_irr_npv_objective_companion

& '..\Run-W109IrrNpvObjectiveCompanion.ps1' `
  -Batch '..\..\work\w109\G6-solvers\batch-irr-npv-objective-companion-discovery-20260809.json' `
  -Out '..\..\work\w109\G6-solvers\validate-only-no-write-irr-npv-objective-20260809.json' `
  -ExpectedBatchSha256 'C114745B446EE166BFD927904BD5158143B52267CB844D8A906275201B7CAA9F' `
  -ValidateOnly
```

The non-`ValidateOnly` runner invocation launches Excel and must not be replayed
without a fresh serialized COM authorization, a fresh zero-process precheck,
and unchanged batch/meta/runner hashes.

### Offline races

```powershell
cargo run --quiet --bin race_irr_npv_objective_companion
cargo run --quiet --bin race_irr_reverse_horner
```

Relevant research-tool hashes at this checkpoint:

| Tool | SHA-256 |
|---|---|
| `src/bin/generate_irr_npv_objective_companion.rs` | `46CB7030DA9630940B3D301A8AC8C68550CBA47D9B822B2E28D8A14109335CC2` |
| `src/bin/race_irr_npv_objective_companion.rs` | `15F39B0BAD91A14E8BF7BB98DD73581F391DF1C78AF5CC93E9373C6297785CB8` |
| `src/bin/race_irr_reverse_horner.rs` | `FD7DBF114C03161CF207A9DAD244FE37122DA9DFDC168B17A8C0D1A1DCEA2CE4` |

## 7. Handoff state

The durable result of this timebox is a sharper decomposition, not an exact IRR
graph:

1. worksheet NPV publication remains a small-ULP structural residue;
2. worksheet evaluator cancellation correction is empirically isolated and
   explicitly ruled out for the internal IRR objective;
3. the best no-snap IRR discovery candidate is 44/72 on the guaranteed two-step
   subset;
4. the 180-row heldout answer surface remains sealed;
5. production, test, formal, catalog, map, workset, and bead integration remain
   untouched.
