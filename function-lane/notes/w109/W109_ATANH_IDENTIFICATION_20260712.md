# W109: ATANH exact graph identification

Status: `closed_signed_off` for the current-reference ATANH slice

Original investigation: `2026-07-12`

Exact-graph supersession and sign-off: `2026-08-09`

Landed implementation: `a03a75f`

## Supersession notice

The July interpretation of the small-input body as an x87
`0.5*(ln1p(x)-ln1p(-x))` pair is retracted. It matched the sparse corpus but
failed the dense candidate-disagreement campaign. The related claims that
subnormal passthrough was emergent and that the small-input body was exactly
odd are also retracted. Current-reference Excel instead observes DAZ for
subnormal inputs and publishes positive zero for both signs.

The July signed-ratio observation was directionally useful but incomplete:
the ratio wrapper is not ordinary binary64. Each add, subtract, and divide is
an x87 PC64 operation followed by a binary64 store, i.e. `RN53(RN64(op))`.

## Identified current-reference graph

For a binary64 input `x`:

```text
a = abs(x)
if a >= 1:
    #NUM!
if a < MIN_POSITIVE:
    +0
if a < f64::from_bits(0x3f1af82b729c1d83):
    x + (x*x*x)/3                         # ordinary binary64 operations
else:
    numerator   = RN53(RN64(1 + x))
    denominator = RN53(RN64(1 - x))
    ratio       = RN53(RN64(numerator / denominator))
    0.5 * excel_log(ratio)                # established x87 LN publication
```

The representative branch threshold is the exact double
`0x3f1af82b729c1d83`. The preceding positive double is cubic, the following
positive double is ratio, and the middle positive double is observationally
equal under both bodies. The corresponding negative middle double selects the
ratio result, so the implementation uses `a < threshold` for the cubic route.
Excel is not globally odd in the ratio region because the signed wrapper is
evaluated independently.

## Black-box evidence

All current-reference captures used worksheet argument cells populated through
`Range.Value2`, `Formula2` formulas referring to those cells, and direct
`Value2` result publication. The sign-off profile was Excel 16.0 build 20228
x64, workbook Compatibility Version 2, `Run-W109BulkBatch.ps1 -NoCache`, and
`cell_value2_bulk`; Excel-process serialization was checked before and after
live batches.

### Dense discovery and exact boundary

- The answer-blind dense switch generator produced `5,902` inputs spanning
  DAZ/subnormal controls, the old transition interval, both signs, adjacent
  doubles, and ratio-wrapper disagreements. The final graph scores
  `5,902/5,902`.
- A 43-step live adjacent-double bisection bracketed the positive transition:
  cubic at `0x3f1af82b729c1d82`, ratio at `0x3f1af82b729c1d84`, with
  `0x3f1af82b729c1d83` equal under both positive candidates.
- The negative seam rows independently select the representative predicate;
  the negative middle double publishes the ratio result.
- Dense subnormal probes show DAZ and positive-zero publication for both input
  signs, refuting the former passthrough claim.

Discovery batch SHA-256:
`A4CB5F73734245C3DC658A2F4932269E6407E1A0CCDE9FE6930D154A48018DD2`.
Discovery answers SHA-256:
`28E8E532539C90CE61655B6AFF28E61A6E5A8A4EF181467B8F57B918016B2799`.
The boundary-bisection artifact SHA-256 is
`D2DC329B39EA5F1E8DEDDBCA8A393C6A0D87B25129956C648FCAF1A244D1BE3F`.

### Held-out refinement and fresh gate

The first frozen 7,050-row set was retired from held-out status after six rows
changed model selection. Those rows exposed DAZ, the negative seam predicate,
and three independent ratio-wrapper staging sites. It remains a durable
refinement corpus.

Across all `2^3` add/sub/div double-rounding masks on the accumulated bank, the
exact counts are:

| wrapper mask | exact / 20,780 |
|---|---:|
| ordinary add/sub/div (`000`) | `19,136` |
| DAZ plus `000` | `20,175` |
| `001` or `010` | `20,266` |
| `011` | `20,357` |
| `100` | `20,598` |
| `101` or `110` | `20,689` |
| x87 double-round add/sub/div (`111`) | **`20,780`** |
| all-extended/no intermediate stores | `15,217` |

After freezing the exact graph, a new answer-blind 8,510-row held-out was
generated. The frozen graph passed `8,510/8,510`; the retired July/v1 model
scored `6,871/8,510`.

Fresh held-out batch SHA-256:
`59A8BC92CEE745FBEA2A40F931A2F3E3623C8D07CC3446205051319778E849F4`.
Meta SHA-256:
`5989B33207C6FA3D28654C241E2D3C8ECA678CEE12816DB329E5CDB1B2440A9D`.
Answers SHA-256:
`0E1B423A0D742712A72DF3BDDEEB1AB9FB64DCD62C4DBF9168356BD26052ECD6`.

The durable scorer
`smart-fuzzer/tools/calc_graph_racer/src/bin/race_atanh_three_regime.rs`
loads the original bank, dense discovery, retired refinement set, and fresh
held-out: `20,780/20,780` distinct typed-bit outcomes.

### Durable evidence inventory

The scorer's seven answer inputs are:

- `G4-hyp-answers-atanh.json` —
  `EA0B8EC41283DBED7B73BF5DCEA16FB21398AE2769EA6B34A6ECD9130B173F61`;
- `G4-02-answers-atanh-band.json` —
  `EAE5D77667EC8485FC1D9BEE5DD2CB715E85ABDED5C594DEC294863CC3E00F74`;
- `G4-02-answers-atanh-gap.json` —
  `71313C1D3542F54C654763E8A374CE7A01C5562E72E5F89405094FF03C27CE53`;
- `G4-02-answers-atanh-switch.json` —
  `F81281CC3D621CD6B67827E5A76D75B481F5D6714927F07B045B1639E7CFAD3C`;
- `G4-02-atanh/answers-atanh-switch-dense-20260809.json` —
  `28E8E532539C90CE61655B6AFF28E61A6E5A8A4EF181467B8F57B918016B2799`;
- `G4-02-atanh/answers-atanh-three-regime-heldout-20260809.json` (retired
  refinement) —
  `8EB189041ED9610ED1606C277F28E01A36213F4076E171BE1EF88675A6DEAD56`;
- `G4-02-atanh/answers-atanh-exact-heldout-20260809.json` (fresh publication
  gate) —
  `0E1B423A0D742712A72DF3BDDEEB1AB9FB64DCD62C4DBF9168356BD26052ECD6`.

The generated current-reference triplets are reproducible as follows:

| cohort | batch SHA-256 | meta SHA-256 | answers SHA-256 |
|---|---|---|---|
| dense `batch/meta/answers-atanh-switch-dense-20260809` | `A4CB5F73734245C3DC658A2F4932269E6407E1A0CCDE9FE6930D154A48018DD2` | `50057642C1C6E2C87B3343C536EB038990202B7C9FD1B8517AB150A77E4319DB` | `28E8E532539C90CE61655B6AFF28E61A6E5A8A4EF181467B8F57B918016B2799` |
| retired refinement `batch/meta/answers-atanh-three-regime-heldout-20260809` | `6592B08865A18476A5E5F88360BA1BC5AEA9DA7FF31799060554F4EE85757998` | `E002CDE7CB3164FF781CCF425A0B6CA3E3136358D62E8A2C01CA842D2BD18CCA` | `8EB189041ED9610ED1606C277F28E01A36213F4076E171BE1EF88675A6DEAD56` |
| fresh gate `batch/meta/answers-atanh-exact-heldout-20260809` | `59A8BC92CEE745FBEA2A40F931A2F3E3623C8D07CC3446205051319778E849F4` | `5989B33207C6FA3D28654C241E2D3C8ECA678CEE12816DB329E5CDB1B2440A9D` | `0E1B423A0D742712A72DF3BDDEEB1AB9FB64DCD62C4DBF9168356BD26052ECD6` |

`G4-02-atanh/atanh-boundary-bisection-20260809.json` hashes to
`D2DC329B39EA5F1E8DEDDBCA8A393C6A0D87B25129956C648FCAF1A244D1BE3F`.

## Implementation and regression gates

Commit `a03a75f` implements the graph in
`crates/oxfunc_core/src/functions/atanh.rs` and adds reusable dense, boundary,
held-out, and replay tooling. Eleven compact pins cover both DAZ signs, the
sign-sensitive threshold neighborhood, and the three independently required
wrapper stores.

- focused ATANH tests: `9/9` passed;
- durable replay: `20,780/20,780` exact;
- full `oxfunc_core`: `1,520` passed, `0` failed, `4` ignored, with all
  integration and doc-test targets passing.

No FEC/F3E admission, coercion, type, shape, or evaluator-facing clause changed,
so no cross-repository handoff is required. The existing ATANH surface metadata
and function binding remain applicable. `formal/lean/OxFunc/Functions/Atanh.lean`
records the identified publication-route order without duplicating the x87
numeric backend; the repair otherwise changes only the Rust numeric kernel and
its black-box evidence/tooling.

## Scoped closure audit

Status axes for the current-reference ATANH calculation-graph slice:

- `scope_completeness: scope_complete`
- `target_completeness: target_complete`
- `integration_completeness: integrated`
- `open_lanes: []` within G4-02. ACOTH remained separate and was subsequently
  signed off independently in `W109_ACOTH_IDENTIFICATION_20260809.md`; other
  elementary/trig rows, alternate application/channel/CPU profiles, locale
  sweeps, and the wider W109/global campaign remain separate open scope.

### OPERATIONS Section 12 — Pre-Closure Verification Checklist

1. Contract/admission surface: pass; unchanged and still applicable, with
   current-reference publication alignment recorded by FDEF-068 as
   `provisional_w109_aligned`.
2. Formal alignment: pass for this slice; the executable route tag records DAZ
   before cubic/ratio dispatch and the stored-x87 ratio route, while the
   established shared x87 helpers remain the Rust executable model.
3. Rust implementation/tests: pass (`9/9` focused; full core `1,520` passed,
   `0` failed, `4` ignored).
4. Deterministic replay: pass (`20,780/20,780`).
5. Evidence/provenance: pass; exact bits, profile, hashes, generators, bisection,
   retired-refinement set, and fresh post-selection held-out are recorded.
6. Version axes: pass for the declared current-reference slice (build 20228,
   CV2); no universal-version claim is made.
7. Public algebra versus empirical behavior: pass; DAZ, the cubic body, exact
   threshold, signed ratio, and wrapper stores follow live Excel evidence.
8. XLL seam limitation: not material to this direct worksheet/core-kernel lane.
9. Cross-repo impact: pass; no handoff required.
10. Known gaps in G4-02: none.
11. Completion-language audit: pass; claims are scoped to G4-02/current profile.
12. Worklist/catalog/state synchronization: pass in this W109 reconciliation;
    the wider campaign remains partial.
13. Bead execution state: pass; `oxf-jwh5.6` is closed without conflating
    BUG-FUNC-027's other still-open subclasses.

### OPERATIONS Section 14 — Completion Claim Self-Audit

1. Scope re-read: pass; only current-reference ATANH G4-02 is claimed.
2. Gate criteria re-read: pass; exact model, live bisection, fresh held-out,
   deterministic replay, landed code, and full tests are present.
3. Silent scope reduction: pass; signs, DAZ/subnormals, exact branch seam,
   wrapper staging, near-domain boundaries, random/dense inputs, and errors are
   represented.
4. Looks-done-but-is-not audit: pass; no tolerance, average-ULP acceptance,
   compile-only path, stale cache, model-selected held-out, or unacknowledged
   handoff supports the claim.
5. Result: pass for the declared G4-02 slice.

The broader W109 and global discrepancy-closure campaign remain
`scope_partial`, `target_partial`, and `integration_completeness: partial`.
