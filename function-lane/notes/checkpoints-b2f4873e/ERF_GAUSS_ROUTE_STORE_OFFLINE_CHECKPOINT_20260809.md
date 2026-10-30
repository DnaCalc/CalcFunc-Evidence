# ERF.PRECISE / ERFC.PRECISE / GAUSS route-and-store offline checkpoint

Date: 2026-08-09

Reference axes are corpus-specific:

- The two GAUSS discovery captures embed Excel 16.0 build 20228, x64,
  Workbook Compatibility Version 2, `cell_value2_bulk`, and NoCache provenance.
- The historical ERF.PRECISE and ERFC.PRECISE WitnessSets used for the paired
  complement audit do not embed per-file application build/channel, bitness,
  Workbook Compatibility Version, input plumbing, or cache provenance. Their
  result is bounded to those reproducible observations and is not a current-
  baseline sign-off.

This tracked checkpoint is a discovery-only increment to
`smart-fuzzer/tools/calc_graph_racer/ERF_GAUSS_EXACT_GRAPH_DISCOVERY_CHECKPOINT_20260809.md`.
It does not promote a production implementation or alter shared documentation,
catalog, map, ledger, BUG-FUNC-027, workset, or bead state. No Excel/COM process
was launched. Both frozen GAUSS heldouts remain absent and sealed.

## Clean-room boundary

The audit uses only:

1. Published TOMS 654 / CDFLIB branch-190 and `gam1` arithmetic.
2. The project's public-semantics Ext80 research emulator.
3. Explicitly named, reproducible W109 ERF.PRECISE, ERFC.PRECISE, and GAUSS
   discovery answers captured through Excel's public automation surface.

The audit source names neither GAUSS heldout answer path and does not read the
historical ERF heldout. No Microsoft binary was inspected.

## Corpus provenance boundary

The GAUSS answer files named below contain `w109-capture-provenance-v1`
objects. They record Excel 16.0 build 20228 x64, Workbook Compatibility Version
2, `cell_value2_bulk`, and NoCache with zero hits and misses. Their batch and
answer IDs and arguments were validated by the governing GAUSS checkpoint.

The seven ERF and five ERFC answer files are older WitnessSets containing only
the function and witnesses. They do not mechanically bind a capture build,
channel, bitness, Compatibility Version, input path, cache mode, or timestamp.
The exact 700/700 directional-complement result is therefore strong historical
black-box evidence for those input/output pairs, but it must not be read as a
build-20228/CV2 assertion. Alternate-version and fresh provenance-rich replay
remain open axes for ERF.PRECISE and ERFC.PRECISE.

Research tool:

```text
smart-fuzzer/tools/calc_graph_racer/src/bin/audit_erf_gauss_route_store.rs
SHA256 374C095A524B9B51502520D94F81D1F1F55D7A96B8964954176B0D939DF1066F
```

The replay fails closed on the expected ERF.PRECISE/ERFC.PRECISE function
names, nonempty unique witness IDs, and scalar arity. For the two GAUSS banks it
also asserts the build-20228/x64/CV2/Value2/NoCache provenance fields before
scoring.

The parent checkpoint SHA256 is
`962B34E38863D4B66CC825E10D36189076BA8F5AA3F363819031A8C04E2B8EB9`.

## ERF/ERFC complement route

The audit joins 1,720 ERF and 870 ERFC nonnegative discovery observations by
exact input bits, yielding 700 same-input pairs. The exact relation on the
banked discovery is directional:

| Input region | Rows | Exact primary relation | Exact | Reverse relation | Exact |
|---|---:|---|---:|---|---:|
| `0 <= x < 0.5` | 513 | `Q = RN53(1 - stored P)` | 513/513 | `P = RN53(1 - stored Q)` | 196/513 |
| `x = 0.5` | 1 | both collapse | 1/1 | both collapse | 1/1 |
| `0.5 < x < 1.375` | 55 | `P = RN53(1 - stored Q)` | 55/55 | `Q = RN53(1 - stored P)` | 16/55 |
| `1.375 <= x < 6` | 130 | `P = RN53(1 - stored Q)` | 130/130 | `Q = RN53(1 - stored P)` | 0/130 |
| `x >= 6` | 1 | `P = RN53(1 - stored Q)` | 1/1 | `Q = RN53(1 - stored P)` | 0/1 |

Thus the direction-selected ordinary binary64 complement is exact on 700/700
paired discovery rows. Replacing it by the compensated binary64 expression
`0.5 + (0.5 - primary)` is exact on only 649/700. This refutes a compensated
publication wrapper on 51 explicit discriminator rows. It also localizes the
remaining `z < 0.5` residual to the primary branch-190 body before complement,
not to ERFC's below-half wrapper.

## GAUSS direct-tiny route/store race

The exact and route discovery answers contribute 3,158 rows with
`abs(x) <= 1e-15`. Symmetry is exact for every nonzero paired observation:

```text
signed pairs                         1,409
nonzero bit-exact odd pairs          1,355/1,355
canonical +0 subnormal-flush pairs      54/54
```

The tool races 11,520 source-backed branch-190/store graphs across all 3,158
rows. The race varies storage of `z^2`, recurrence and `J`, public `gam1(1/2)`
arithmetic mode, storage of `g`, compensated/direct inner subtraction,
multiplication association and first-product storage, recovery of `w`, and five
equivalent placements of the exact factor 1/2.

The best aggregate is:

```text
exact       2,822/3,158
max ULP     1
sum ULP     336
histogram   expected-minus-model {-1: 170, 0: 2822, +1: 166}
ties        480 graphs at the same aggregate score
```

This improves the preceding checkpoint's best zero-limit/effective-normalizer
score of 2,638/3,158 (maximum 2 ULP, sum 531) to 2,822/3,158 (maximum 1 ULP,
sum 336). The improvement comes from carrying the already identified stored
GAUSS argument `z = RN53(abs(x) * FRAC_1_SQRT_2)` into the full public
branch-190 body, including `J`, rather than reducing the route to an adjusted
constant.

All best graphs use the published `gam1(1/2)` rational with every arithmetic
operation staged to binary64 and then form `g = 1 + h` in Ext80. The closest
alternatives are materially separated:

| `gam1` arithmetic | Exact | Maximum ULP | Sum ULP |
|---|---:|---:|---:|
| binary64 per operation | 2,822/3,158 | 1 | 336 |
| Ext80 continuous | 2,324/3,158 | 2 | 885 |
| Ext80 with binary64 returned `h` | 1,706/3,158 | 1 | 1,452 |

The current tiny inputs do not distinguish direct reuse of stored `z` from the
public x87-continuous `sqrt(z^2)` route: both score 2,822/3,158, maximum 1 ULP,
sum 336. The five half-placement families also tie, as expected for an exact
binary scaling at these magnitudes. These are discovery ambiguities, not an
exact survivor.

Magnitude split for one representative best graph:

```text
abs(x) < 4*EPSILON     2,478/2,644
abs(x) >= 4*EPSILON      344/514
```

## Deterministic replay

Run from `smart-fuzzer/tools/calc_graph_racer`:

```powershell
rustfmt --edition 2024 --check src/bin/audit_erf_gauss_route_store.rs
cargo run --release --offline --bin audit_erf_gauss_route_store -- C:\Work\DnaCalc\OxFunc
```

The release replay passed. Capturing its UTF-8 PowerShell `Out-String` stdout
produced 45 lines and SHA256
`87AC470FCB7FAC06EF91217639E360933D588EB8266198533FD886EF85E1414E`.

GAUSS discovery answer hashes:

```text
answers-gauss-exact-discovery-v1.json  8BFFAF353EFFDB54F15B82CCA4997E35761E4F65A51A0991B169C1CA75AFBCA8
answers-gauss-route-discovery-v1.json  2D225BDB490FC8B6EF980B68B5993ACE4E69F97262D60885F4C7CBDF9E1FD1B1
```

ERF discovery answer hashes:

```text
answers-b9train.json  92A52BAB7B3921EC89881664DA746243C470A4963607E3F53DBBD21885757ECC
answers-erfp.json     E39ACD64ED89F60DB5DA51E2E4D2CFBC5959905E3608029C16240F33695A772C
answers-erfm.json     9224FF64096F1994A5A6F10CBC8A5E67BDD8976DF3FAB2C016C891D3A1C27BEC
answers-b8erf.json    72A277F5A53138231F6C49591621EF55B7E1AAA366099ECCD6F8B0942711D423
answers-b7erf.json    12842C7992944391C584DDFF39AA5E77796FDC7198B6DF1747EEFCF420AB4FCF
answers-b11.json      6AEC3CE19AF4B7FA7120B551D8FB06C685393FD3171EA801B2C6315EB305CA62
answers-b10.json      A89BB4D238EF6F02D4E65B89624A4FC5CCA896114C0E277B3E32C5ADCA07F909
```

ERFC discovery answer hashes:

```text
answers-erfcp.json   DE3ACD0291DA1BB9F9827A664256EED1AE0A5B2998A530DFF98DC28BED3378DB
answers-erfcm.json   9CDDB0FD254974E9205624EE738D55BE9EC8998C61532D0E7205C3A38C0E3D72
answers-b8erfc.json  9041CD3AA84F034EB441A158979765C93F077E3ECB108605B027BD8B895F4C21
answers-b7erfc.json  F0B20AAB8A4133F2F97BB4D15A298BDBC34C23F170C6EB61D618637C18A73885
answers-b11c.json    B363DFA855FBA2D50AD55F1212146144B1DD21409CF6FAFA3756ADDD5DB4783D
```

## Gate and status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`

`open_lanes`:

1. Resolve the 336 one-ULP direct-tiny residuals with one coherent public graph.
2. Separate the 480 aggregate-tied store/association graphs using existing
   candidate disagreements before considering another answer-blind oracle bank.
3. Resolve the six decoded-Q branch-190 landmark residuals and the broader
   ERF tooth/comb observations.
4. Resolve the ERFC mid/tail body and boundary graph.
5. Produce exact discovery survivors for ERF.PRECISE, ERFC.PRECISE, and GAUSS.
6. Execute the two frozen GAUSS heldouts only after a coherent exact discovery
   survivor and explicit serialized root authorization.
7. Production, test, formal-model, shared state, and catalog integration remain
   gated on an exact frozen heldout and root authorization.

No new COM request is frozen by this checkpoint. Candidate-disagreement mining
against the existing discovery is the next offline discriminator.
