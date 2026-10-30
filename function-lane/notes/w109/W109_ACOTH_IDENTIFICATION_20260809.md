# W109: ACOTH exact graph identification

Status: `closed_signed_off` for the current-reference ACOTH G4-03 slice

Identification, frozen gate, and production verification: `2026-08-09`

Implementation state: landed in commit `7f7eac9`.

## Supersession notice

The July interpretation of ACOTH's far-field body as an x87
`0.5*(ln1p(1/|x|)-ln1p(-1/|x|))` pair is retracted. It improved the sparse
corpus but missed `ACOTH(5)` and the exact `8.1` witness. ATANH's independently
identified cubic/ratio graph also proves that ACOTH cannot inherit the former
`excel_atanh_small` helper. That helper and its stale ATANH-labelled comments
have been removed.

Current-reference Excel instead uses a direct inverse odd-power series in the
far field. The exact ACOTH graph was identified independently through
answer-blind candidate-disagreement generators, live `NoCache` captures, an
exact adjacent-double switch search, and a candidate frozen before a fresh
disjoint held-out.

## Identified current-reference graph

For a binary64 input `x`, let `a = abs(x)`:

```text
if a <= 1:
    #NUM!

if a < f64::from_bits(0x400d92b14ec204f3):
    numerator   = a + 1                         # native binary64
    denominator = a - 1                         # native binary64
    ratio       = RN53(RN64(numerator / denominator))
    magnitude   = 0.5 * excel_log(ratio)       # x87 FYL2X publication
else:
    reciprocal = RN53(RN64(1 / a))
    if reciprocal < MIN_POSITIVE:
        magnitude = +0
    else:
        square = RN53(RN64(a * a))
        power  = a
        sum    = reciprocal
        for k = 1 .. 31:
            power       = RN53(RN64(power * square))
            denominator = RN53(RN64((2*k+1) * power))
            term        = RN53(RN64(1 / denominator))
            next        = RN53(RN64(sum + term))
            stop if next == sum
            sum = next
        magnitude = sum

if magnitude == 0:
    +0
else:
    copysign(magnitude, x)
```

The representative branch threshold is the exact double
`0x400d92b14ec204f3`, whose shortest decimal is `3.69662725`. The last
ratio-distinguishing positive input is `0x400d92b14ec204ef`
(`3.69662724999999837`); the first series-distinguishing positive input is the
threshold itself (`3.69662725000000014`). Their bit gap is four. The three
intermediate doubles are observational overlap because both bodies publish the
same bits there.

The direct-ratio additions/subtractions are ordinary binary64; only the ratio
division is the stored x87 PC64 operation. In the series, every reciprocal,
multiply, divide, and accumulator add is stored through x87 PC64-to-binary64
double rounding. Storing `excel_log(ratio)` before multiplication by the exact
power-of-two factor `0.5` is bit-equivalent on this normal result range to
retaining the half-scale in the x87 register.

## Black-box evidence and provenance

All current-reference captures used numeric argument cells populated through
`Range.Value2`, `Formula2` formulas referring to those cells, and bulk
`Value2` result readback. The sign-off profile was Excel `16.0`, build `20228`,
64-bit, workbook Compatibility Version `2`, Windows x86-64,
`Run-W109BulkBatch.ps1` version `w109-bulk-batch-v2`, PowerShell `7.6.3`,
`cell_value2_bulk`, and `-NoCache` with cache hits/misses both zero. Each answer
artifact embeds this provenance.

Excel/COM ownership was serialized with the W109 lanes. Every ACOTH capture
started from `EXCEL_PROCESS_COUNT=0`, completed with all requested numeric
rows and no errors, reached bounded teardown `EXCEL_PROCESS_COUNT=0`, and was
explicitly released before another lane launched:

| cohort | numeric rows | pre | post |
|---|---:|---:|---:|
| dense discovery | `18,284/18,284` | `0` | `0` |
| graph discovery | `29,344/29,344` | `0` | `0` |
| switch round 1 | `79,100/79,100` | `0` | `0` |
| switch round 2 | `75,842/75,842` | `0` | `0` |
| frozen exact held-out | `66,552/66,552` | `0` | `0` |

### Discovery and switch identification

The discovery bank exercised domain edges, both signs, exponent strata,
subnormal reciprocal publication, ratio wrapper store masks, direct-series
operation stores, term schedules, broad random inputs, and dense adjacent-bit
seam ladders. Across the legacy bank plus dense, graph, and two switch rounds,
the frozen graph scores `202,217/202,217` distinct signed inputs exactly.

On positive route discriminators, `97,958` rows uniquely select one body,
`3,369` are overlap, and there are zero anomalies. The exhaustive remaining
49,152-double seam bracket in switch round 2 pinned the adjacent
distinguishing endpoints above.

### Frozen held-out gate

`generate_acoth_exact_heldout.rs` encoded the candidate and selection grammar
before any held-out answers existed. It excluded every one of the `202,217`
prior signed input bit patterns and deterministically generated `66,552` new
rows from disjoint random seeds, full exponent strata, IEEE boundary ladders,
the frozen route seam, and frozen-body calculation-graph discriminators.

The frozen candidate passed `66,552/66,552` exactly. On positive held-out route
discriminators, `22,610` rows uniquely select a body, `10,666` are overlap, and
there are zero anomalies. No model refinement was performed from held-out
answers.

The durable combined scorer loads the legacy bank and all five current capture
cohorts. Both its independent frozen research graph and the actual production
`acoth_kernel` score `268,769/268,769` distinct signed inputs exactly. The
combined positive classification is `120,568` route-discriminating rows,
`14,035` overlap rows, and zero anomalies.

## Reproducible artifact inventory

Base directory:
`smart-fuzzer/work/w109/G4-03-acoth/` (gitignored working evidence; hashes are
promoted here so the captures remain independently identifiable).

The original legacy answer bank
`smart-fuzzer/work/w109/G4-hyp-answers-acoth.json` hashes to
`053F2D14D148734BE1CC3105F2571525C0075641BEAF4072CD9A4BFF94342A99`.

| cohort (`batch` / `meta` / `answers`) | batch SHA-256 | meta SHA-256 | answers SHA-256 |
|---|---|---|---|
| `acoth-dense-discovery-20260809` | `9E5572CDAC27D0C97828499D49817D3696C746851A7A624C8258429BB25E03EE` | `1AB0185A24455FC728BEF1E605C45BA977BD9063E384CDD0CC39FF1540A3B19C` | `9F029E1A0EEED00B43479EC9608D6BD473A2B2BB527323DAD226B1EB117693D5` |
| `acoth-graph-discovery-20260809` | `6667FC0AD879E0FE8635D6B3FDC14F66F5B8B4E43A4A9385787EA60703EBD1A2` | `FEDDFF5138CE90C2C1DD27FF5651043092A34439E54BAEC26852A438D287E97D` | `2E19A00EEF05C30F46691917DCF809730BDF22F3B8B3D727EA95EBC3940B1AAD` |
| `acoth-switch-r1-20260809` | `E5C7372F7EFBD7176C1828CE22E4577A377A7D5425433DAA84F151BC2EADDD9A` | `5D1C238466173E31628128D8F8C19250839CDC5741D460B55E1A1D3E1B20B435` | `8937A350356C14D3A675DD2DB7AB2D5BD4B26C17A3E1CAEDED22AAA8032AC487` |
| `acoth-switch-r2-20260809` | `19751A55C9B26965C16A675D7B237B8C0920C03725E45924817C8D8BF4EE973E` | `B7FB3EFB704B230A3D456C24F35E04B58A70032DFDB99ECB70B709EF0B22E123` | `F079688B50F77CBA0EC45A37AD239FF94FAB83F16B7163CDA700FA2E484E8F46` |
| `acoth-exact-heldout-20260809` | `34D93AA30F411DE64F87BF5F3A8CD73F9AA14567E3DC10784D9E480157AA8A62` | `27943F61C3D38786E15EA6D9992EB1B1C1A0A1D93E5BA794ADF6901A5B1A97A8` | `91E0B5EBA4AC5058789545BEA1190A4F2AA5BB97B1AA3877F332129BB66B6F4B` |

Durable source tooling under
`smart-fuzzer/tools/calc_graph_racer/src/bin/`:

- `race_acoth_exact.rs` — explicit reciprocal/log/publication candidate racer;
- `generate_acoth_dense_discovery.rs` — broad first discriminator generator;
- `race_acoth_series.rs` — direct/reciprocal series graph racer;
- `generate_acoth_graph_discovery.rs` — per-operation staging discriminators;
- `generate_acoth_switch_round.rs` — deterministic switch rounds;
- `score_acoth_switch.rs` — frozen graph classifier plus asserted production replay;
- `generate_acoth_exact_heldout.rs` — answer-free, prior-disjoint frozen gate.

## Production, formal alignment, and regression gates

`crates/oxfunc_core/src/functions/acoth.rs` now implements the exact graph and
pins the domain, near-one publication, both routes, exact seam endpoints,
mid-range series discriminators, oddness, and positive-zero reciprocal flush.
The obsolete `excel_atanh_small` helper and its stale ATANH-labelled comments
were removed from `crates/oxfunc_core/src/excel_numeric/mod.rs`; exact ATANH
does not use that helper, and exact ACOTH uses the direct inverse-power series.
The Rust kernel, exact pins, Lean route binding, and seven reusable research
tools landed together in `7f7eac9`.

`formal/lean/OxFunc/Functions/Acoth.lean` records the executable route order
(`reciprocalFlushPositiveZero`, `storedX87RatioLog`, and
`storedX87InverseOddPowerSeries`) without duplicating the x87 numeric backend.

Verification:

- focused ACOTH tests: `7/7` passed;
- full `cargo test -p oxfunc_core`: library `1,523` passed, `0` failed,
  `4` ignored; every integration and doc-test target passed;
- frozen research graph replay: `268,769/268,769` exact;
- actual production kernel replay: `268,769/268,769` exact;
- all seven ACOTH racer/generator binaries: release `cargo check` passed with
  no warnings;
- `lake build`: `492` jobs passed;
- exact-file `rustfmt --check` and `git diff --check`: passed.

No FEC/F3E admission, coercion, type, shape, host, or evaluator-facing clause
changed, so no OxFml handoff is required. XLL verification-seam limits are not
material to this scalar core-kernel lane.

## Scoped closure audit

Status axes for the current-reference ACOTH G4-03 calculation-graph slice:

- `scope_completeness: scope_complete`
- `target_completeness: target_complete`
- `integration_completeness: integrated`
- `open_lanes: []` within G4-03. Alternate application/channel/CPU profiles,
  locale sweeps, other BUG-FUNC-027 subclasses, and the wider W109/global
  campaign remain separate open or orthogonal scope.

### OPERATIONS Section 12 — Pre-Closure Verification Checklist

1. Contract/admission surface: pass; unchanged and still applicable, with
   current-reference publication alignment recorded by FDEF-070.
2. Formal alignment: pass; the Lean route tag records positive-zero flush
   before ratio/series dispatch and both stored-x87 graph families.
3. Rust implementation/tests: pass (`7/7` focused; full core and every
   integration/doc-test target green).
4. Deterministic replay: pass (`268,769/268,769` frozen and production).
5. Evidence/provenance: pass; exact bits, profile, process counts, hashes,
   generators, model-selection history, and fresh held-out are recorded.
6. Version axes: pass for the declared build-20228/x64/CV2 slice; no
   universal-version claim is made.
7. Public algebra versus empirical behavior: pass; the direct inverse series,
   exact seam, per-operation stores, and positive-zero publication follow live
   Excel even where algebraically equivalent log forms disagree.
8. XLL seam limitation: not material to this scalar worksheet/core-kernel lane.
9. Cross-repo impact: pass; no FEC/F3E or evaluator-facing handoff is required.
10. Known gaps in G4-03: none.
11. Completion-language audit: pass; claims are scoped to G4-03/current profile.
12. Worklist/catalog/state synchronization: pass in this reconciliation; the
    wider W109 campaign remains partial.
13. Bead execution state: pass; `oxf-jwh5.7` is closed without conflating the
    still-open BUG-FUNC-027 aggregate or W109 epic.

### OPERATIONS Section 14 — Completion Claim Self-Audit

1. Scope re-read: pass; only current-reference ACOTH G4-03 is claimed.
2. Gate criteria re-read: pass; answer-blind discovery, exact switch,
   candidate-frozen disjoint held-out, deterministic replay, production code,
   full tests, and formal alignment are present.
3. Silent scope reduction: pass; signs, domain boundaries, near-one inputs,
   route seam, ratio/series staging, exponents, reciprocal underflow, exact
   positive-zero publication, and broad random cases are represented.
4. Looks-done-but-is-not audit: pass; no tolerance, average-ULP acceptance,
   compile-only path, stale cache, held-out model refinement, scaffolding, or
   unacknowledged handoff supports the claim.
5. Result: pass for the declared G4-03 slice.

The broader BUG-FUNC-027 stream, W109, and global discrepancy-closure campaign
remain `scope_partial`, `target_partial`, and
`integration_completeness: partial`.
