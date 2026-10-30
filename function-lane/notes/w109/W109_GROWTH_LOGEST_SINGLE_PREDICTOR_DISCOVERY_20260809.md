# W109: GROWTH/LOGEST single-predictor discovery

Status: `in_progress`; G3-03 and G3-04 remain open

Investigation date: `2026-08-09`

This record preserves a current-reference, single-predictor numeric discovery
campaign for `LOGEST` and `GROWTH`. It retracts an underdetermined July claim,
records bounded-negative calculation-graph races, and defines the next probe
lanes. It is not a held-out sign-off packet and does not authorize a production
or formal-route change.

## Status axes

- `scope_completeness=scope_partial`
- `target_completeness=target_partial`
- `integration_completeness=partial`
- `open_lanes=[exact coefficient/reduction schedule; normal/subnormal
  publication; fractional POWER/product staging; multivariate inputs; complete
  const=false behavior; omitted/default known_x and new_x; orientation and
  result shape; coercion/errors/order; prior-disjoint held-out; production,
  tests, formal alignment, and state integration]`

## Retraction and current result

The former claim that `GROWTH(x)=b*m^x` is bit-exact whenever the published
`LOGEST` factor/base cells are supplied was inferred from two integer-prediction
controls. Those two controls are underdetermining: 240 of 23,328 enumerated
graphs reproduce both. The combined current-reference discovery bank rejects
that claim as a complete graph.

On 1,240 numeric `GROWTH` cells, the best tested reconstruction from the live
published `LOGEST` cells is raw worksheet-x87 power followed by a stored-x87
multiply, at only `666/1240` exact. The best direct internal
`EXP(a+b*x)` candidate is `610/1240`; an internal-coefficient raw-power/product
candidate is `494/1240`. No tested single-predictor graph is exact.

The structural rows are more decisive. All 20 `GROWTH` `#NUM!` outcomes in the
refinement set are reproduced by coefficient-publication followed by
POWER/product candidates, while the best direct-log graph reproduces only two
and misses 18. Therefore `GROWTH` cannot generally be modeled as one final
`EXP(a+b*x)` over continuously retained internal coefficients.

## Current-reference captures

Two answer-blind discovery rounds were captured serially with zero Excel
processes before launch and after bounded teardown. Both use Excel `16.0`,
build `20228`, 64-bit, workbook Compatibility Version `2`, matrix `Value2`
plumbing, and `NoCache`.

| round | `LOGEST` calls | `GROWTH` calls | result summary |
|---|---:|---:|---|
| paired discovery v1 | `200` | `700` | all numeric; IDs/arguments aligned |
| refinement v2 | `160` | `560` | `LOGEST`: 158 numeric + 2 `#NUM!`; `GROWTH`: 540 numeric + 20 `#NUM!`; IDs/arguments aligned |

The second round is discovery/refinement evidence, not a held-out set. Its 80
prior-disjoint datasets target LN providers, row-order/unroll behavior,
coefficient EXP publication, and prediction association.

## Combined score table

| layer | exact numeric | structural match | maximum ULP | sum ULP |
|---|---:|---:|---:|---:|
| `LOGEST` factor | `139/180` | n/a | `28` | `112` |
| `LOGEST` base | `135/178` | `2/2` | `258` | `1622` |
| paired `LOGEST` coefficients | `270/358` | `2/2` | `258` | `1760` |
| direct internal `EXP(a+b*x)` | `610/1240` | `2/20` | large structural mismatch | large structural mismatch |
| internal coefficients, raw power/product | `494/1240` | `20/20` | large structural mismatch | large structural mismatch |
| observed `LOGEST`, raw x87 power + stored-x87 multiply | `666/1240` | `20/20` | large structural mismatch | large structural mismatch |

The selected `LOGEST` factor and base candidates use different accumulator and
provider schedules. Their combined coefficient score is only `270/358`
numeric plus `2/2` structural, so the coefficient kernel itself remains open.

## Metamorphic observations

- `GROWTH(x=0)` equals the observed `LOGEST` base in 80 of 83 occurrences;
  two additional occurrences are paired `#NUM!` outcomes.
- The remaining occurrence publishes a positive subnormal `LOGEST` base
  (`0x00015f8d01430ccc`), while `GROWTH(0)` publishes `+0` and the nonzero
  translated predictions publish `#NUM!`. This exposes a distinct publication
  or underflow route.
- `GROWTH(x=1)` equals `base*factor` in all nine numeric controls; that narrow
  identity does not determine fractional-exponent staging.
- In the v2 length lane, factor cells are equal for `16/16` reversal pairs and
  base cells for `15/16`; prediction equality holds for `79/90` comparable
  cells. The broader v1 bank remains order-sensitive (`LOGEST` coefficient
  equality `30/50`, `GROWTH` equality `89/175`).
- A selected `n=3..18` prefix slice admits tied `64/64` coefficient models,
  but this is a discovery-only local overlap and not function-wide evidence.

## Reproducible tooling

Tracked source candidates for this checkpoint are:

- `smart-fuzzer/tools/calc_graph_racer/src/bin/growth_research/common.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/growth_research/refinement_v2.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/race_growth_existing.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_growth_paired_discovery.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/score_growth_paired_discovery.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/analyze_growth_paired_residuals.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/race_growth_centered_refinement.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/generate_growth_refinement_v2.rs`
- `smart-fuzzer/tools/calc_graph_racer/src/bin/score_growth_refinement_v2.rs`

The final handoff artifact
`smart-fuzzer/work/w109/G3-04-growth/handoff-refinement-v2.json` embeds and
checks the source inventory and the v2 artifact inventory. Selected Cargo
checks, exact-file formatting checks, deterministic generator replay, and the
handoff hash cross-check pass.

## SHA-256 inventory

### Source

| artifact | SHA-256 |
|---|---|
| `growth_research/common.rs` | `A0FC652CE2497F1C6A2D258CE9438C3C4E946E4BE6842D490515E49ABAAEC780` |
| `growth_research/refinement_v2.rs` | `4131131AEACE47BFF2E3DA906178BBC5920ED2880FE5051524E4CC6D9D5974E5` |
| `race_growth_existing.rs` | `EBA9F918271448E7BDE1219A8162E93D92F07C9C11A1B98801347F573D9F9680` |
| `generate_growth_paired_discovery.rs` | `F7DD27DE1A9418AC41F78F1E7AC8675D79160FB1275726A376DC5AD5318FC243` |
| `score_growth_paired_discovery.rs` | `BEFB078693253172BEB3C3672FF3D196B069DA83CDE909838361741572DA91C2` |
| `analyze_growth_paired_residuals.rs` | `35936616F0E468595FACCFBBE0AD7923119AF63F75D52A5C378DF965E38EE27C` |
| `race_growth_centered_refinement.rs` | `C1E29D01508EAC9ECE8645FAA43FE9F17C78C2E58DD96DB60863BC18B79F777B` |
| `generate_growth_refinement_v2.rs` | `FA1CEFF9EA1EA62FC54D468A3BAA6F395FA22F29CFA521D4CC321A9002D5B9D8` |
| `score_growth_refinement_v2.rs` | `BB8743B5F41D034060A99B76841E7F83EB9491C4A540001D85B489670F83459C` |

### Live batches and answers

| artifact | SHA-256 |
|---|---|
| `batch-logest-paired-discovery-v1.json` | `33044F296CEE2C2090374CBACD168D6F8172D7CC611645C0001237CA5F05EC7B` |
| `answers-logest-paired-discovery-v1.json` | `DBF185671F0FD56685F2E16EAEA2C850C63E9E1220DA738BB57DC0ECBED005E0` |
| `batch-growth-paired-discovery-v1.json` | `21B73573268AC973EC1615E68C04F2C1CBB88098D2B6F4AD4814019216A4E0A2` |
| `answers-growth-paired-discovery-v1.json` | `039056992574C64CB5293C9EBDB3F28A3C2F85D397300FF0559D9CBDFAB600CD` |
| `batch-logest-refinement-v2.json` | `7C7667BAF05D167C6DD4BAE56131DF9154C7F0905FFF97D0CCE60ADB88C384CC` |
| `answers-logest-refinement-v2.json` | `022C46D8992F479661BB644C963048E7C8DC47AB6B3381A965BFFE83D488F5B5` |
| `batch-growth-refinement-v2.json` | `B598FC4D62694E24310181BFC31D38BBE7D0BC604CC7208F442688FE221F5AAE` |
| `answers-growth-refinement-v2.json` | `4EE2FF4F6367B75A5C6A3E151FC4F180E02037C0D28AF07A7C80002FCD1F1076` |
| `candidate-manifest-refinement-v2.json` | `B39ABE91EA4A3DE538238F4B14F3B650D555517B7B343F4D7142B5CFB71DEE10` |
| `meta-refinement-v2.json` | `AE88B202EB3E1B859096BAD0EEA78FB3153E84FB5352866B845A27320A88E72F` |
| `score-refinement-v2.json` | `503FD901775E276716B9504D6CD6B8F3F6378A3C28ACDB040A3B0A0E8AA00CA3` |
| `handoff-refinement-v2.json` | `0A526A5FA73583FCB5728F9FF47B0903BB29BB11519E9EE09FD1C5807DED5F23` |

## Next probes

The next useful scalar probe is not another generic prediction grid. It should
hold the chosen accumulator schedule fixed and target the remaining
length-dependent coefficient associations, the subnormal publication seam,
and fractional-exponent POWER/product store windows. Any survivor then needs a
fresh prior-disjoint held-out gate. Full-function promotion additionally
requires the multivariate, omitted/default, orientation/shape,
`const=false`, coercion, error, and ordering axes listed above.
