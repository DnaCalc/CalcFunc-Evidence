# W109: COMBINA exact graph and combinatorial admission identification

Status: `closed_signed_off` for the current-reference `COMBINA` sublane of the
mixed G4-04 row, with a scoped admission correction to the already identified
`COMBIN` body

Identification, frozen gates, implementation, and verification: `2026-08-09`

Implementation commit: `3f31f44`

The enclosing G4-04 row remains open only for `ERF`/`ERF.PRECISE` and
`ERFC`/`ERFC.PRECISE`. This report makes no closure claim for those functions
or for the wider W109 campaign.

## Historical claim retracted

The July claim that every product graph for `C(26,7)` must publish the exact
integer, and that `COMBINA` therefore had to use `GAMMALN`, was too broad. The
later `COMBIN` work identified a cyclic product whose quotient and accumulator
stores are double-rounded from x87 PC64 to binary64. That graph can publish an
inexact floating-point integer.

A clean re-audit against broad-scalar cycles 010--015 found that the exact
stored-x87 `COMBIN` graph applied to the separately truncated transformed
arguments is `143/143` exact on the historical numeric rows. The former
multiply-first `COMBINA` implementation is only `35/143`. The GAMMALN
attribution and the claimed product impossibility are retracted.

## Identified current-reference route

For finite binary64 inputs on Excel 16.0 build 20228 x64/CV2:

```text
n0 = DAZ(n)
k0 = DAZ(k)
tn = trunc_toward_zero(n0)
tk = trunc_toward_zero(k0)

if tn == 0 and tk == 0:
    return 1
if tn < 0 or k0 < 0:
    return #NUM!

return COMBIN_KERNEL(tn + tk - 1, tk)
```

`DAZ` maps either-sign binary64 subnormals to signed zero. The zero/zero pool
precedes the asymmetric negative-choice guard. The total is constructed only
after each source argument has been truncated, so this route is not generally
the worksheet-visible composition `COMBIN(n+k-1,k)`, where addition happens
before `COMBIN` truncates its arguments.

`COMBIN_KERNEL` is the existing cyclic stored-x87 graph, now with its inherited
admission layer pinned:

1. DAZ both inputs, reject remaining raw negative inputs, and truncate toward
   zero.
2. Admit a first argument through `2_147_483_646`; the next integer is
   `#NUM!`, including when the choice is zero.
3. Reject `k>n`, reduce `k=min(k,n-k)`, and return one when the reduced choice
   is zero.
4. For ascending `i=2..k`, store `(n-k+i-1)/i` and each accumulator multiply
   through x87 PC64-to-binary64 double rounding, then multiply by `n` through
   the same stored operation.
5. Return `#NUM!` as soon as the accumulator becomes nonfinite. Every factor
   after complement reduction is greater than one, so this cannot hide a later
   finite publication and prevents an admitted near-central 32-bit input from
   taking roughly a billion iterations after overflow.

Direct Rust calls with NaN or either infinity return `#NUM!` defensively.
`Range.Value2` cannot inject those values, so that guard is seam qualification,
not an Excel-observed behavior claim.

Representative guard pins include:

- `COMBINA(-0.25,0.75) -> 1`, but `COMBINA(-0.25,1) -> #NUM!`;
- `COMBINA(1,-0.25) -> #NUM!`;
- `(1,-min_subnormal) -> 1`, but `(1,-min_normal) -> #NUM!`;
- `(-min_subnormal,1) -> #NUM!` and `(+min_subnormal,1) -> #NUM!`;
- transformed total `2_147_483_646` is admitted and `2_147_483_647` is
  `#NUM!`.

## Black-box evidence and provenance

All current-reference captures used Excel 16.0 build 20228, 64-bit, workbook
Compatibility Version 2, bulk `Range.Value2` argument injection and result
readback, `cell_value2_bulk`, and `-NoCache`. Every authorized capture began
with zero Excel processes, asserted the function, count, unique IDs, ordered
IDs and exact argument bits, and completed bounded teardown with zero Excel
processes.

### Central graph discovery and publication gate

| corpus | role | selected production replay |
|---|---|---:|
| COMBINA identity discovery | frozen discovery, 35,201 numeric + 32 `#NUM!` | `35,233/35,233` |
| COMBINA central held-out | candidate-frozen, prior-disjoint | `2,048/2,048` |

On the numeric discovery rows the former multiply-first production route is
`7,810/35,201`. On the 2,048-row held-out the declared controls score:

| declared model | exact |
|---|---:|
| selected separately-truncated stored-x87 COMBIN route | `2,048/2,048` |
| former production product | `164/2,048` |
| native PC53 cyclic graph | `1,658/2,048` |
| continuously retained x87 graph | `228/2,048` |
| forward factor order | `287/2,048` |
| worksheet composition with addition before truncation | `1,792/2,048` |

Every declared held-out family is exact only for the selected route. No model
was refined after the held-out answers were opened.

### Admission discovery

The initial 213-row edge battery produced only 16 numbers and 197 `#NUM!`
outcomes. It decisively refuted the provisional `i64` transform wrapper but was
too coarse to locate the guard. A frozen paired boundary sweep then captured
2,692 `COMBINA` rows and 2,003 transformed-total `COMBIN` controls:

- current production is `2,692/2,692` and `2,003/2,003` exact;
- all 701 fixed-transformed-total decomposition groups agree;
- 2,335 of 2,399 valid paired links agree exactly;
- the 64 deliberate differences are negative fractional-choice cases where
  `COMBINA` rejects before delegation while the transformed `COMBIN` control is
  numeric;
- the paired controls locate the inherited `COMBIN` first-argument ceiling at
  exactly `2_147_483_646`.

### Retired v1 and fresh v2 admission publication gate

The first frozen COMBIN-only admission gate is retained as discovery evidence,
not publication evidence. Its predeclared candidate scored `108/116`: eight
negative-subnormal rows returned one in Excel and exposed shared DAZ before
the COMBIN negative-domain guard. A clean recapture is hashed below; after the
DAZ correction production replays it `116/116`. The companion COMBINA v1 batch
was never opened.

Fresh v2 COMBIN and COMBINA batches were generated disjoint from every prior
row, including v1, after the shared-DAZ rule was frozen. The unmodified
candidate passed without refinement:

| fresh v2 gate | selected | declared controls |
|---|---:|---|
| COMBIN | `76/76` | no-DAZ `66/76`; raw-value ceiling `62/76` |
| COMBINA | `144/144` | no-DAZ `139/144`; guard-before-zero-pool `136/144`; addition-before-truncation `120/144` |
| combined | `220/220` | selected exact in every family |

The fresh gate includes `.25`/`.75` values on both sides of the 2^31-derived
ceiling, choices 0/1/2, both-sign subnormal/min-normal discriminators, and the
zero-pool/negative-guard ordering pins.

### Artifact hashes

Base directory: `smart-fuzzer/work/w109/G4-04-combina/` (gitignored evidence).

| artifact | SHA-256 |
|---|---|
| `batch-combina-identity-discovery-v1.json` | `318F5DF0D98E787D6209ECB5F80ECFAF4ACD417B774D4FF4C8B12363A7D6F2A9` |
| `batch-combina-identity-discovery-v1.meta.json` | `8B7C7D5839E506EB7B1E3483E65E1A8B20B142893B0FDE10C549471034E5E45B` |
| `predictions-combina-identity-discovery-v1.json` | `11CF476401A5BF13BD6E307A862E3675D5516FA73AC618907A9F395BA4841F40` |
| `answers-combina-identity-discovery-v1-excel.json` | `B622C239E0B8536D542D3D96BF6E2F886E4940805BA85CA3F8A363752DDEB5D5` |
| `batch-combina-identity-heldout-v1.json` | `E336B7D97823C5159E45AFF021ABF319FE39281F2EC9881F9BA50899241BE625` |
| `batch-combina-identity-heldout-v1.meta.json` | `D5B909FB439D52B56AEB8C73E4B24236F0B7EA18F2FA4267CBFBC1EF0C3C1063` |
| `predictions-combina-identity-heldout-v1.json` | `6429011EB0FF3839D646EC79F44E199B8E06CB201FAEBD0C6B6021B2EF6075E6` |
| `answers-combina-identity-heldout-v1-excel.json` | `333A6437E894928AB205BE8C8D1CE284531B928F7592458D71151022FA04D33F` |
| `batch-combina-transform-edge-discovery-v1.json` | `94E8A9BE2B7C83E95FBB012A6D1113E659707713498BD04E91BD793AA1A3D8B0` |
| `answers-combina-transform-edge-discovery-v1-excel.json` | `169BC1945303C8BB249321E437CF826003252B126686FEDA9983ABA64A8D7893` |
| `batch-combina-admission-boundary-discovery-v1.json` | `6FA295A625F9ED7097D473D3BF22E009AF3D12246D8FC8ABCEEBEB39630D2C78` |
| `answers-combina-admission-boundary-discovery-v1-excel.json` | `06437E3B2BDF24A988A9C2A39CBE74F6A1423DAA171C96350F5DC3C15A474F51` |
| `batch-combin-transformed-boundary-control-discovery-v1.json` | `558EE595CFCA02A549254E0170D5BBC8DEC953665A1F5E0DC245875F376D0900` |
| `answers-combin-transformed-boundary-control-discovery-v1-excel.json` | `C9CBC554B7863EC5971D7CFC5FD30AB5892D2FE8B6FCCD83C1F226A4C54452C2` |
| `batch-combin-admission-heldout-v1.json` (retired) | `43190F8B1C659DB350B44036847505E9A51E311E11A45C5015BA62ABD8FA1EBF` |
| `predictions-combin-admission-heldout-v1.json` (retired) | `E75EA9ED49E8E9C42A8D331106AF7A219838B087E1F40889460F87D44D8881BE` |
| `answers-combin-admission-heldout-v1-excel.json` (retired) | `BBD92CCC024C7338110FFCC53D1D9D6702D87CE32E9FD08CE1FCFDC2B6D29910` |
| `batch-combin-admission-heldout-v2.json` | `20BCA19D0B03DF0C259429674DE37FD17ABDB28066551C88DA96C30DFEA5912B` |
| `batch-combin-admission-heldout-v2.meta.json` | `6DD4E9CABB15462AEF29547E6E1D1BADEC29C2455763105DED78DFC0BCD4776B` |
| `predictions-combin-admission-heldout-v2.json` | `2A310F577C07EDEE3B44BEE6BF2B859D1F45D27E69140F4A555C5DFDFACC7EDD` |
| `answers-combin-admission-heldout-v2-excel.json` | `3608BF467D49ED22EF73D00F5C8F6FE0778AC88A550D49B17961B721FB655CFC` |
| `batch-combina-admission-heldout-v2.json` | `52E6B40EA8A89254961025D1CF02A8E544FCEA4D87BBB53B6AD45E3DFAADD996` |
| `batch-combina-admission-heldout-v2.meta.json` | `BE611D538A97DD72EC90FE4023F2C84974B8DFC60ACFD018C5279907B154A4BB` |
| `predictions-combina-admission-heldout-v2.json` | `2BC371D04C8843EA61B61252663D509ECADCD472EB0880C722EA00AB4DF22174` |
| `answers-combina-admission-heldout-v2-excel.json` | `BD1D59AC2B25C47F983907E99E5E736BCC4CF13EB583FE60951BBBD55A5FF0C8` |

Tracked clean-room source hashes after exact-file formatting:

| source | SHA-256 |
|---|---|
| `smart-fuzzer/tools/calc_graph_racer/src/bin/race_combina_combin_identity.rs` | `B9C0543D4954E1F485443DE2940654D8A2956E43572CC39D35D56CA0EB32506C` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_combina_identity_batches.rs` | `EEB2385647D86799FD28E9CF7101AEE0812980B97446C46CAD3964E98C9AA8A7` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_combina_transform_edges.rs` | `E0EC88BB3EDFA2CFACDBAE6D0560AB119FDCC71C2CED04B01EBCB4D2A7DFE8E1` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_combina_admission_boundary.rs` | `067FE34C1F3AB34F66EE1C4A190F726C65BF72BF79292F729CE42BF55BC83459` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/analyze_combina_admission_boundary.rs` | `89A7FBBE7D6C940081E11B1919544A7177440B7B6B72B0A9473707A0EBBB315F` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_combina_admission_heldout.rs` | `347037C58029CB1956E35EF72F91600F2D9355C753E0D1A91BFD76F329A7FACE` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_combina_admission_heldout_v2.rs` | `CDFF9A49E2723D0DB85B48726B5D994D4D70FEF76F5C4E19C78B4ECA44FBBACB` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/score_combinatorics_frozen_predictions.rs` | `83AEB4D88FA4AB69924A6D93AD44D93810F57283E6430988FBA423C1FA39343A` |
| `smart-fuzzer/tools/calc_graph_racer/src/bin/score_combinatorics_typed_batch.rs` | `592AC06AD5166D38FCA06BAEFCF52761247B1402657937E47112406EAA3BCEA0` |

These generators, analyzer, and typed scorers assert deterministic IDs, exact
ordered argument bits, function and result kinds, and answer-blind prediction
files. They never invoke Excel during scoring.

## Production and formal alignment

The integration package changes:

- `crates/oxfunc_core/src/functions/combina.rs`, replacing the former exact
  integer product with the identified DAZ/truncation/guard/transform route;
- `crates/oxfunc_core/src/functions/combin.rs`, adding shared DAZ, the exact
  first-argument ceiling, defensive nonfinite admission, and the monotone
  overflow short-circuit without changing the signed-off cyclic body;
- `formal/lean/OxFunc/Functions/Combina.lean`, binding the executable surface
  guard order and inherited COMBIN route;
- `formal/lean/OxFunc/Functions/Combin.lean`, binding the corrected admission
  and monotone nonfinite route.

Verification:

- focused Rust combinatorics tests: `23` passed;
- full `cargo test -p oxfunc_core`: green, including `1,541` library tests and
  all integration/doc-test targets, with zero failures;
- current production COMBINA replay: `40,330/40,330` exact;
- new/shared COMBIN admission replay: `2,195/2,195` exact;
- original COMBIN corpora retained: `22,242/22,242` exact;
- combined original/new typed replay: `64,767/64,767` exact;
- focused Lean modules: green;
- full Lean: `492/492` jobs;
- exact-file formatting and exact-path `git diff --check`: passed.

No FEC/F3E admission, coercion, type, shape, host, or evaluator-facing clause
changed. No OxFml handoff is required, and the XLL verification seam is not
material to this scalar numeric route.

## Scoped closure audit

Status axes for `COMBINA` on the declared current reference:

- `scope_completeness: scope_complete`
- `target_completeness: target_complete`
- `integration_completeness: integrated`
- `open_lanes: []`

Status axes for the corrected `COMBIN` admission plus its retained body are the
same: `scope_complete`, `target_complete`, `integrated`, with no current-target
open lane.

Status axes for the enclosing G4-04 row and W109 campaign:

- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `open_lanes`: `ERF`/`ERF.PRECISE`, `ERFC`/`ERFC.PRECISE`, remaining catalog
  rows, broad post-catalog discovery, and declared application-version/
  Compatibility-Version axes.

### OPERATIONS Section 12 — Pre-Closure Verification Checklist

1. Contract/admission surface: pass; `FDEF-071` records corrected shared COMBIN
   admission and `FDEF-072` binds COMBINA's exact route.
2. Formal alignment: pass; the executable surface and route tags record DAZ,
   truncation, guard order, transformed total, inherited ceiling, and cyclic
   publication schedule; focused and full Lean builds are green.
3. Rust implementation/tests: pass; focused and full suites are green.
4. Deterministic replay: pass; production is `64,767/64,767` across the
   retained original and all new typed corpora.
5. Evidence/provenance: pass; exact bits and kinds, capture profile, process
   counts, answer-blind selection, retired-v1 discipline, controls, and hashes
   are recorded.
6. Version axes: pass for the declared build-20228/x64/CV2 target; older COMBIN
   overlap is retained without a universal version claim.
7. Public algebra versus empirical behavior: pass; the separately truncated
   transform and intentionally inexact stored graph replace the false GAMMALN
   attribution.
8. XLL seam limitation: not material.
9. Cross-repo impact: pass; no evaluator seam changed and no handoff is needed.
10. Known semantic gaps: none for COMBINA or corrected COMBIN admission on the
    declared current reference.
11. Completion-language audit: pass; claims are scoped to those functions and
    target; G4-04/W109 remain partial.
12. State synchronization: pass; the canonical catalog, map/ruled-out ledger,
    FDEF rows, evidence registry, bug stream/register, workset, worklist, and
    finding reports are synchronized while the enclosing row remains open.
13. Bead state: pass; scoped child `oxf-jwh5.11` is closed signed off without
    closing parent `oxf-jwh5`.

### OPERATIONS Section 14 — Completion Claim Self-Audit

1. Scope re-read: pass; the current-reference COMBINA and shared COMBIN
   admission scope is explicit; ERF/ERFC and wider W109 are not claimed.
2. Gate criteria re-read: pass; deterministic discovery, disjoint frozen
   held-outs, edge/admission qualification, implementation, formal alignment,
   regression pins, and full verification are present.
3. Silent scope reduction: pass; numeric and `#NUM!` kinds, fractions, signed
   zero/subnormal/min-normal, zero pool, both guard orders, totals, choices
   0/1/2, 2^31 ceiling, large central overflow, and cyclic publication are
   covered.
4. Looks-done-but-is-not audit: pass; v1 is explicitly retired, v2 is genuinely
   fresh and exact without refinement, and no tolerance or compile-only result
   is used.
5. Active-surface and bead audit: pass; synchronized surfaces retain the
   mixed-row qualification and the scoped child does not close W109.
6. Result: pass for the declared current-reference COMBINA sublane and the
   scoped shared COMBIN admission correction.
