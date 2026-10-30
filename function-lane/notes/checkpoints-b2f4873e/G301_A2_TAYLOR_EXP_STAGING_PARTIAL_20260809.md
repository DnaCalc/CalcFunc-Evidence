# W109 G3-01 `a = 2` Taylor / EXP-staging offline race (2026-08-09)

## Status

- `execution_state: in_progress`
- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `open_lanes:` exact internal `t1` delivery, exact series-body arithmetic,
  final publication, independently frozen discovery, sealed heldout, production,
  replay, and formal/integration evidence

No production, doctrine, catalog, map, bead, or shared-state file was changed.
No Excel process was launched. No new oracle batch was frozen because no
candidate survived the existing answer-blind discovery subset exactly.

## Question and clean slice

The existing G3-01 record contains two statements which need to be read
together:

1. the catalog still names the `a = 2` Taylor micro-staging as open; and
2. the July identification report later calls the then-enumerated family
   exhausted and reports `38/45` for forward Cephes-form summation with the
   series-site chopped x87 EXP.

The `a = 2`, `beta = 1`, cumulative `GAMMA.DIST` slice with `0 < x < 2`
removes the fractional-gamma normalizer entirely: `Gamma(2) = 1` exactly and
the input is already the internal `y`. It therefore isolates

```text
t1 = 2*ln(x) - x
r  = exp(t1)
P  = (r/2) * (1 + x/3 + x^2/(3*4) + ...)
```

subject only to argument delivery, EXP publication, recurrence arithmetic,
and final publication.

All evidence used here is clean-room: already-captured black-box Excel
answers, the public TOMS-654/NSWC series structure already transcribed in the
repository, and execution of the documented x87 arithmetic/transcendental
instructions through the repository research surface. No Microsoft binary was
inspected.

## Exact scorer and evidence identity

Scorer:

`smart-fuzzer/tools/calc_graph_racer/src/bin/race_g301_a2_taylor.rs`

- bytes: `34,928`
- SHA-256: `2A3E98370CA93D4061C829839BDE32131EB342376D3168C298ACE19AF5C8A9AA`

The scorer filters exact binary64 arguments, asserts that duplicate inputs
have identical Excel answers, and deduplicates by `x` bits. The resulting
bank has `27,144` unique rows:

| Cohort | Rows | Role |
|---|---:|---|
| legacy (`b5` + modern baseline) | 45 | reproduces the July `38/45` claim |
| `b23A` | 1,499 | cross-view logarithmic grid |
| `b23B0..B5` | 24,000 | six dense EXP-reduction windows |
| `b26A` | 900 | moderate uniform clean-series grid |
| `b26X` | 700 | moderate logarithmic cross-view grid |

Evidence hashes:

| File | SHA-256 |
|---|---|
| `answers-b5.json` | `5406DADBBC2639E9034F0FC84DAC3A88A87D83EB31AF21A8E159EC86DC3B1614` |
| `answers-gammadist-modern.json` | `86E1547514264423E84C7829646ADA3159D5202D12AD23A610E55AF15F9CEBCC` |
| `answers-b23-gd.json` | `553FFCDCE770D8E3A88327BE13D3B8B660D69CBEFF204EFEDB192BABF0D91473` |
| `answers-b26-gd.json` | `B54AC2C18E368BB6C0472A2892FEE42FB6A67B8940F9853EE9EF8399F9FE483D` |
| `batch-b5.json` | `259854F5632DCA0A616A75FDF631CC656B835EAE35522576A9618E39A80A56D3` |
| `batch-gammadist-modern.json` | `82BD3DF4D195E384EF95119F3777A6DA9DE3A6BAED9A0768E917DCAA147EE8B1` |
| `batch-b23-gd.json` | `77A4AC8D80A1A3E4C79F9189EB284F3D300D120AF7BCC6A193E4CE0EA87A1320` |
| `batch-b26-gd.json` | `20A099798D611C813C2885821DA42141095BC16FFFAC2205E2B71B0BAD4E6CF3` |

These are historical July captures. The adjacent W109 record attests Excel
16.0 build 20131 for the July campaign and later records the bulk-recalculation
path, but the old `WitnessSet` answer schema binds neither assertion per file
and embeds no capture provenance. In particular, workbook Compatibility
Version, bitness, channel, cache mode, and capture method are not mechanically
bound to these answer files. This lane therefore treats them as historical
discovery evidence and keeps the reference-version axes open.

The deterministic discovery subset is answer-blind: all legacy and b26 rows,
plus b23 rows satisfying `x_bits % 29 == 0`. It contains `2,459` rows. This is
an offline ranking subset of already-read evidence, not a new candidate-frozen
oracle gate.

## Candidate family

The racer scores `10,808` legal graphs assembled from:

- eight `t1` deliveries: stored `std`/worksheet/raw-x87 logarithms, raw-x87
  multiply/subtract with stored or extended `t1`, standard-log input widened
  into a raw extended subtract, and fused-double control;
- seven EXP modes: standard nearest; real x87 PC64 nearest, toward-zero,
  upward, or extended delivery; and PC53 nearest/toward-zero controls;
- thirteen series schedules: forward division-first/multiplication-first,
  tail-then-one, reverse, pairwise, Kahan, distributed `1/2`, NSWC backward,
  per-op x87-double-rounded, and register-continuous x87 controls; and
- f64, continuous-x87, per-op-double-rounded, and directed intermediate/final
  publications for `(r/2)*ans`, `(r*ans)/2`, `r*(ans/2)`, additive, and
  distributed-factor forms.

## Results

### Production reconciliation

Current production scores:

| Cohort | Exact | Max ULP |
|---|---:|---:|
| legacy | `38/45` | 2 |
| b23 | `6,603/25,499` | 40 |
| b26 | `795/1,600` | 4 |
| all unique | `7,436/27,144` | 40 |

The scorer's explicit graph

```text
stored f64 std-ln t1
-> x87 PC64 EXP published RZ53
-> forward division-first double series
-> f64 (r/2)*ans
```

replays current `regularized_gamma_p(2,x)` on `27,144/27,144` rows with zero
kernel disagreements. Thus the July `38/45` number and the current production
implementation are reproduced exactly; the broader bank shows that this is a
partial approximation, not an exact a=2 realization.

### Answer-blind discovery

- exact survivors: `0/10,808`
- best graph: `1,323/2,459`, max 4 ULP, ULP-distance sum 1,682

The best graph is the coherent clue:

```text
std ln(x) stored as f64
-> PC64 x87 (2*ln(x)-x) retained extended into fFEXP
-> EXP published RZ53
-> forward division-first series with every arithmetic op x87-PC64 then RN53
-> final nearest publication
```

The best clean-b26 score over all `10,808` graphs is only `820/1,600`, max 4
ULP. The same graph family wins, but it misses 780 clean rows.

### Full bank

Every graph was re-scored on all `27,144` unique rows. The global maximum in
this family is:

| Cohort | Exact | Max ULP |
|---|---:|---:|
| legacy | `39/45` | 1 |
| b23 | `14,440/25,499` | 30 |
| b26 | `820/1,600` | 4 |
| all unique | `15,299/27,144` | 30 |

Residual histogram for that graph:

```text
-30:1 -29:6 -28:2 -27:1 -14:1 -13:2 -4:1 -2:246 -1:4994
 +1:3465 +2:2450 +3:458 +4:218
```

Subgroups and input bands remain inconsistent:

| Slice | Exact | Max ULP |
|---|---:|---:|
| b23A | `889/1,499` | 4 |
| b23B | `13,551/24,000` | 30 |
| b26A | `433/900` | 4 |
| b26X | `387/700` | 4 |
| `0 < x < 0.01` | `5,276/9,095` | 30 |
| `0.01 <= x < 0.1` | `3,027/4,186` | 4 |
| `0.1 <= x < 0.3` | `84/119` | 2 |
| `0.3 <= x < 1.6` | `6,912/13,731` | 4 |
| `1.6 <= x < 2` | `0/13` | 3 |

The extended-`t1` / per-op-double-rounded graph is therefore a strong
directional clue, not a survivor. It more than doubles aggregate exact hits
relative to current production, but its mixed-sign residual and total failure
on the sparse upper band prohibit a production or closure claim.

## Reconciled verdict

1. The catalog's statement that Taylor micro-staging remains open is supported.
2. The July `38/45` and production graph are faithfully reproduced.
3. “Family exhausted” can only describe the narrower family tested at that
   time; it cannot support an exact-staging claim over the now-banked a=2
   scope.
4. RZ53 publication of the PC64 x87 EXP remains the strongest EXP axis.
5. A standard-log value followed by an unspilled extended `t1` subtraction is
   substantially stronger than every stored-`t1` delivery tested, while a raw
   extended logarithm is worse. This localizes the next search to the boundary
   between logarithm return, `a*L-x`, and EXP entry rather than to a different
   Taylor summation family.
6. No new COM capture is justified yet: there is no exact discovery survivor
   to freeze, and both large dense banks and clean moderate banks already
   reject the tested family.

## Next bounded lever

If this lane is resumed, build implied-prefactor intervals from the exact
Excel result and each deterministic series sum, then synthesize adjacent-`x`
discriminators where stored-`t1`, extended-subtract, and EXP-entry variants
predict disjoint intervals. Include deliberate coverage near `x in [1.6,2)`,
where the present best graph is `0/13`. Freeze that batch before reading any
new answers and keep a separate heldout sealed. Do not alter production until
one coherent graph is exact on the frozen discovery and an independent
heldout.

## Verification command

```powershell
cargo run --release --manifest-path smart-fuzzer/tools/calc_graph_racer/Cargo.toml --target-dir target-g301-a2 --bin race_g301_a2_taylor -- smart-fuzzer/work/w109/G3-01-dist
```

The release build and deterministic replay passed on the reference host.
