# W109 G3-02 GAMMALN/GAMMA high-band offline scope-partial report

Date: 2026-08-09

Execution mode: offline replay only. This tracked checkpoint did not start Excel, use COM,
write an answer bank, edit production code, edit shared doctrine/state/beads, or
stage/commit files.

## Three-axis status

- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `execution_state: in_progress`

Open lanes:

1. `GAMMALN x>=8`: identify the sub-binary64/staging source of the two remaining
   one-ULP rows. The coherent graph below is not an exact semantic identity.
2. `GAMMALN other bands`: outside this assigned lane and still governed by the
   broader G3-02 status.
3. `GAMMA positive x>=8`: distinguish a retained-extended `lgamma -> exp`
   composition from a direct gamma kernel.
4. `GAMMA negative/reflection/overflow/domain lanes`: outside this bounded
   replay.
5. Production integration, production tests, canonical records, and bead state
   were not authorized in this lane.

## Corpus and provenance audit

### Current-build GAMMALN capture

The current-build batch and answer bank agree in function name and in all 64
ordered `(id, args)` pairs. The answer bank contains 62 numeric witnesses, two
`error:Num` witnesses, and 28 numeric `x>=8` witnesses.

Recorded provenance in the answer bank:

- schema: `w109-capture-provenance-v1`
- captured UTC: `2026-08-09T13:22:20.5038883Z`
- Excel version/build: `16.0` / `20228`
- bitness: `64-bit`
- Workbook Compatibility Version: `2`
- input plumbing: `cell_value2_bulk`
- cache: `no_cache`, hits `0`, misses `0`
- runner: `Run-W109BulkBatch.ps1`, `w109-bulk-batch-v2`

### Historical GAMMALN union

The 12 historical banks named in the replay command below deduplicate to 6,076
numeric `x>=8` inputs with zero conflicting expected bit patterns. Those banks
do **not** contain the current capture-provenance object, so their application
build, channel, bitness, Workbook Compatibility Version, input plumbing, and
cache state are not independently recoverable from the JSON files.

Adding the current-build bank produces 6,092 unique numeric `x>=8` inputs with
zero conflicts. The current bank contributes 16 unique high-band inputs and
overlaps the historical union on 12. This cross-bank agreement is useful
behavioral evidence, but it does not retrofit missing provenance onto the
historical banks.

### Historical GAMMA bank

`answers-r0.json` contains 72 positive numeric `GAMMA` rows with `x>=8`, all of
which have an exact input-bit match in the historical GAMMALN union. This GAMMA
bank also lacks a capture-provenance object. Therefore the wrapper result below
is a historical bank inference, not a current-build sign-off.

## Reconstructed high-band graph

Let `DR(op)` mean: execute the indicated operation through the repository's
clean-room x87 PC64/RN model and then store/round to binary64. Let `LN87(x)` be
the already identified worksheet-LN `FYL2X` result stored to binary64.

```text
ln   = LN87(x)
q1   = DR((x - 0.5) * ln)
q2   = DR(q1 - x)
q    = DR(q2 + LS2PI)

z    = 1.0 / x                         # native binary64
y    = z * z                           # native binary64
w    = W6
w    = w*y + W5                        # native binary64, five Horner steps
w    = w*y + W4
w    = w*y + W3
w    = w*y + W2
w    = w*y + W1
corr = z * w                           # native binary64
out  = DR(q + corr)
```

Constants are the public fdlibm `e_lgamma_r` `w1..w6` binary64 values already
present in `crates/oxfunc_core/src/excel_numeric/gammaln.rs`; `LS2PI` is
`0x3fed67f1c864beb5`. The research race also includes a Cephes A5 tail, the
first six exact Bernoulli asymptotic coefficients as a control, documented
Windows CRT `log`/`tgamma` APIs, and a clean-room double-double atanh-series log.
No binary image was inspected.

### Scores

| Replay | Exact | Worst absolute ULP | Sum absolute ULP |
|---|---:|---:|---:|
| Current production high band | 18/28 | 2 | not emitted by frozen scorer |
| Frozen candidate-v1 (worksheet LN, otherwise native q/tail) | 24/28 | 2 | not emitted by frozen scorer |
| Reconstructed graph, current build | 26/28 | 1 | 2 |
| Reconstructed graph, historical 12-bank union | 6074/6076 (99.9670836076%) | 1 | 2 |
| Reconstructed graph, current + historical union | 6090/6092 (99.9671700591%) | 1 | 2 |

The exact same two input bit patterns are the only misses in all three graph
replays:

| Current ID / historical ID | Input bits | Decimal x | Stored LN bits | Got | Expected | ULP delta |
|---|---|---:|---|---|---|---:|
| `old-resid-02` / `fill-b4hi-0664` | `0x40215bf4d43f4d44` | 8.67960227272727280 | `0x400149ada19738a3` | `0x4023d98694477878` | `0x4023d98694477879` | -1 |
| `old-resid-03` / `fill-b4hi-1613` | `0x40234ce3244e3245` | 9.65017045454545475 | `0x400222c417a0e7e3` | `0x40280a8dd6771c99` | `0x40280a8dd6771c9a` | -1 |

## Bounded negative searches

1. At both residual inputs, worksheet x87 LN, Rust/std UCRT `ln`, `libm::log`,
   `msvcrt`, `msvcr100`, `msvcr110`, `msvcr120`, and `ucrtbase` return the same
   binary64 log bits shown above.
2. Bumping that stored log input by integer binary64 ULPs skips the target at
   both residuals: bump `0` publishes delta `-1`; bump `+1` publishes delta
   `+1`. The target therefore lies between the effects of adjacent stored-log
   values for this graph.
3. `LS2PI` neighbors from -32 through +32 ULP do not improve 26/28.
4. The q-only race contains no graph that reaches either residual.
5. The 110,592 tail/final graphs vary `z`, `y`, each of five Horner multiply/add
   sites, correction formation, and final addition across native binary64,
   x87-PC64-with-store, one-store multiply/add, and FMA families. The best bank
   score stays 26/28; zero graphs reach either residual.
6. Best public-tail family scores are fdlibm 26/28 (worst 1, sum 2), exact
   Bernoulli 21/28 (worst 6, sum 22), and Cephes A5 20/28 (worst 33, sum 107).
7. A full `3^12 = 531,441` state grammar per log source assigns each graph node
   PC53, PC64 plus binary64 spill, or PC64 continuous. Residual-only hits are
   numerous but do not survive full-bank ranking:

   | Log state | Per-residual hits | Hits both | Best current-bank survivor |
   |---|---|---:|---|
   | x87 LN stored binary64 | `[177147, 118098]` | 118098 | 19/28, worst 1, sum 9 |
   | x87 LN retained extended | `[187353, 118098]` | 118098 | 12/28, worst 2, sum 17 |
   | clean-room DD log retained extended | `[187353, 118098]` | 118098 | 12/28, worst 1, sum 16 |

This rejects the bounded all-PC53/PC64 store-state grammar as a universal exact
explanation. It does not prove that every possible public arithmetic graph has
been exhausted.

## GAMMA wrapper implication

For the 72 historical positive `x>=8` GAMMA rows:

| Candidate | Exact | Worst absolute ULP | Sum absolute ULP |
|---|---:|---:|---:|
| Current production gamma kernel | 0/72 | 1370 | 24441 |
| Published/best-bank GAMMALN -> identified worksheet EXP | 1/72 | 623 | 11953 |
| Published/best-bank GAMMALN -> std/UCRT exp | 1/72 | 623 | 11955 |
| Published/best-bank GAMMALN -> `libm::exp` | 1/72 | 623 | 11956 |
| `libm::tgamma` | 5/72 | 54 | 800 |
| `msvcr120::tgamma` | 4/72 | 54 | 775 |
| `ucrtbase::tgamma` | 4/72 | 54 | 775 |

An EXP-input inversion searched +/-4,096 binary64 input ULPs around each paired
published GAMMALN result. Only 2/72 GAMMA targets are exactly reachable by a
stored binary64 `lgamma` input (one at bump 0, one at bump +1). The other 70/72
targets lie strictly between worksheet-EXP outputs for adjacent binary64 inputs;
none falls outside the search and the maximum crossing distance is two input
ULPs.

Therefore this historical GAMMA bank is inconsistent with a simple
`stored-binary64 published GAMMALN -> identified worksheet EXP` wrapper on
70/72 rows. The remaining coherent hypotheses are a retained-extended
log-gamma/exponent composition or a direct gamma kernel. The direct public
`tgamma` APIs are much closer than the wrapper candidates but are not exact.

## Replay gates

Run from the repository root in PowerShell.

### Gate 1: source format

```powershell
rustfmt --edition 2024 --check smart-fuzzer/tools/calc_graph_racer/src/bin/race_gammaln_highband_residual.rs
```

Expected: exit 0, no output.

### Gate 2: offline release build

```powershell
$env:CARGO_TARGET_DIR='C:\Work\DnaCalc\OxFunc\target-gamma-highband'
cargo build --offline --release --bin race_gammaln_highband_residual `
  --manifest-path smart-fuzzer/tools/calc_graph_racer/Cargo.toml
```

Expected: exit 0.

### Gate 3: frozen current-build baseline

```powershell
py -3.7 smart-fuzzer/work/w109/G3-02-gamma/score_gammaln_current_build_discovery.py `
  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-current-build-discovery-v1.json
```

Expected high-band summaries: production `18/28`, worst 2; candidate-v1
`24/28`, worst 2.

### Gate 4: current-build reconstructed graph

```powershell
& target-gamma-highband/release/race_gammaln_highband_residual.exe --base-only `
  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-current-build-discovery-v1.json
```

Expected lead summary: `26/28 exact worst=1 sum=2`, with only `old-resid-02`
and `old-resid-03`.

### Gate 5: historical union

```powershell
$banks = @(
  'smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-r2.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-dense1.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-g12dense.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-peel.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-precise.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-zeros.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-L-boundary.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-L-core.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-L-round3.json',
  'smart-fuzzer/work/w109/G3-02-gamma/answers-b32-gammaln.json',
  'smart-fuzzer/work/w109/G4-04-combin/answers-gammaln.json'
)
& target-gamma-highband/release/race_gammaln_highband_residual.exe --base-only $banks
```

Expected lead summary: 6,076 unique rows, zero conflicts, `6074/6076 exact
worst=1 sum=2`.

### Gate 6: bounded state grammar and broad tail race

```powershell
& target-gamma-highband/release/race_gammaln_highband_residual.exe `
  --base-only --state-search `
  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-current-build-discovery-v1.json

& target-gamma-highband/release/race_gammaln_highband_residual.exe `
  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-current-build-discovery-v1.json
```

Expected state hit counts and 110,592-graph reachability are recorded above.

### Gate 7: historical GAMMA implication

```powershell
& target-gamma-highband/release/race_gammaln_highband_residual.exe `
  --base-only --gamma-bank smart-fuzzer/work/w109/G3-02-gamma/answers-r0.json `
  $banks
```

Expected: 72 paired rows; best direct API `libm::tgamma` at 5/72; stored-lgamma
inversion exact 2, skipped-between-adjacent-EXP 70, outside 0, max crossing 2.

## SHA-256 manifest

Repository HEAD observed during this lane: `265c4e396cb53a5ba804047e9c995f3ba7a4e4ce`.
The working tree was already dirty, so the hashes below, not HEAD alone, define
the replay inputs used here.

```text
e56f55db0c439d0b9b909f0be6b92299b156b224f0c92b451fc21eac0fa41faa  smart-fuzzer/tools/calc_graph_racer/src/bin/race_gammaln_highband_residual.rs
3d5cb6290eb963e70b50b54618d3d9a34f4c0f08e20c91f44c37d4319c81ff8f  target-gamma-highband/release/race_gammaln_highband_residual.exe
a71ffae003d4f4b9fd90c1678920a6d132c0f1566c95fd3c720a482b36bd0a02  smart-fuzzer/tools/calc_graph_racer/Cargo.toml
812920dbba3c03f5d02c2dfcb504bd306fd51289400a4432c20ed6dc39dc6094  smart-fuzzer/tools/calc_graph_racer/Cargo.lock
7bc85577690c84d41fb9b7055af76e908158f9293e1365110b30fc9db30aa92b  crates/oxfunc_core/src/excel_numeric/gammaln.rs
db43632b1c68febff0538bb5c058033f55360533e36f813bc762bbfc846689ab  crates/oxfunc_core/src/excel_numeric/research.rs
e87e6d3eeea599a7d24c1a66eec0c6403993cf774458018939fe3bbd7961b059  crates/oxfunc_core/src/functions/special_dist_family.rs
e021a309d84d06aaca10bbeac4f3fbe845b12998727001479879f86446766404  smart-fuzzer/work/w109/G3-02-gamma/score_gammaln_current_build_discovery.py
c555cb3e044991cc0746e87158871807c35880c6d26624f1997526cc32092a3d  smart-fuzzer/tools/calc_graph_racer/target/release/check_gammaln_port.exe
3b785fffa16009e5613e1d7ae589a2f666de4ee28123dce317a3f648bd340455  smart-fuzzer/tools/calc_graph_racer/target/release/x87_serve.exe
578898bd4720fe0d1c9fcbb4312a12a8cc31c5c55822d95a7cb196dcbd1374be  smart-fuzzer/work/w109/G3-02-gamma/batch-gammaln-current-build-discovery-v1.json
1dd40f55e3b995730e800aebd0ef3c2f646bc01bbc08a525ff9a671431335f44  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-current-build-discovery-v1.json
bb3fbdde1ff01508a36988d6de7b21cac5641dfde8b30fbca3f867e73e447380  smart-fuzzer/work/w109/G3-02-gamma/answers-r0.json
d3775beafadfbe43b48c8ac073eb0d4bfb93582b73e3fe2f5aee083965522514  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln.json
005a6280dcfddfb177d24d6a2c296179d3abf0bcc7f37f2136afcfe5f0d2ad6f  smart-fuzzer/work/w109/G3-02-gamma/answers-r2.json
adc0eb0d01ae52b8ca68ab72c911e0d91dd157dae9c89f599c29679dca6e12d1  smart-fuzzer/work/w109/G3-02-gamma/answers-dense1.json
7d3f7f2ce2badbcdab99ab0c898a5ece78a2516994054c997d1b7edce43bd4ab  smart-fuzzer/work/w109/G3-02-gamma/answers-g12dense.json
02c01b5fd9e370e4dfb56f3ae8850cd108ebc55ca3083e8ff18b65231f6a1cef  smart-fuzzer/work/w109/G3-02-gamma/answers-peel.json
4621efa36788642f7159b78e12574c58241d91363dd722417ece6b121460f93b  smart-fuzzer/work/w109/G3-02-gamma/answers-precise.json
d12ffbd3b74fb909c8915c6d9d013cef69632d1575c63292d02544ad8904328e  smart-fuzzer/work/w109/G3-02-gamma/answers-gammaln-zeros.json
4e4b73b3b785322f4a234c43558c9953226eafcfe32f261c419e0ce44c8867f0  smart-fuzzer/work/w109/G3-02-gamma/answers-L-boundary.json
c7466f103613eac0bfe2813bddd918708e0f0a7dbe83aaad8ae17a5b87ea83b9  smart-fuzzer/work/w109/G3-02-gamma/answers-L-core.json
ee437a89a5335833a0475a47118015c04ad7b9f745e94f6638f6b1f2f24f1c52  smart-fuzzer/work/w109/G3-02-gamma/answers-L-round3.json
e02a198e9c6a8286404a8dfe64afffc5f7e7b53787beb85e94bc3f7b5c15f5cb  smart-fuzzer/work/w109/G3-02-gamma/answers-b32-gammaln.json
924feca2df4d383c3df5c13d5dde53a50ac4d727f2d6096ada6a11ce64752d3e  smart-fuzzer/work/w109/G4-04-combin/answers-gammaln.json
```

## Frozen capture request

None. The two residual inputs are already present in the current-build
NoCache/CV2 capture, and the bounded search produced no competing full-bank
survivor whose identity can be cleanly separated by a small new batch. A new
capture should be designed only after a sub-binary64 or direct-kernel survivor
exists; no COM action is requested by this report.
