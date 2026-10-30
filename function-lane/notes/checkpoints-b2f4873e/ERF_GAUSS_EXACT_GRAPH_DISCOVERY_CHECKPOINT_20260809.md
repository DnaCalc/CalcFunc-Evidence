# ERF.PRECISE / ERFC.PRECISE / GAUSS exact-graph discovery checkpoint

Date: 2026-08-09
Reference application axis: Excel 16.0 build 20228, x64
Workbook compatibility axis: CV2

This is a discovery-only clean-room checkpoint for catalog lanes G4-04 and
G3-07. It records public-source graph races and reproducible black-box behavior.
It does not promote a production implementation or update the shared catalog,
map, ledger, BUG-FUNC-027, workset, or bead surfaces.

## Method and provenance boundary

Allowed evidence used here:

1. Published TOMS 654 / CDFLIB `gratio` and `gam1` arithmetic.
2. Public fdlibm, Cody/CALERF, NSWC/CDFLIB, Boost, and host-libm controls.
3. Existing reproducible W109 discovery observations.
4. Two answer-blind, deterministically generated GAUSS discovery captures made
   through Excel's public automation surface by the serialized root lane.

No Excel or Microsoft binary was disassembled, decompiled, dumped, or otherwise
inspected. The research programs explicitly name discovery answers only. Neither
GAUSS heldout has an answer file, reader path, score, or publication decision.
The historical `answers-b9heldout.json` is excluded from every score in this
checkpoint.

## Frozen current-build GAUSS banks

| Role | Rows | Batch SHA256 | Answer SHA256 / state |
|---|---:|---|---|
| exact discovery v1 | 8,192 | `8627F7E248545CB618684EFA24D76336BBE9C6A545B7BCFE2CE2D9CE3F3395A3` | `8BFFAF353EFFDB54F15B82CCA4997E35761E4F65A51A0991B169C1CA75AFBCA8` |
| exact heldout v1 | 4,096 | `D10E8B813BAABD6F7718ED78E6008FDC2D75CC0C2B272AEEC25487949F2E21D4` | absent and sealed |
| route discovery v1 | 1,024 | `28F0BEBFBF5354A5624DAC7B0C6A27EF01E74ADD10E85DF513C0DC51E6EE4F93` | `2D225BDB490FC8B6EF980B68B5993ACE4E69F97262D60885F4C7CBDF9E1FD1B1` |
| route heldout v1 | 512 | `E6F737337C3F1661A48E362D9333D4E0B09DF564F6CFEFB1C62BCD80B68DAFF0` | absent and sealed |

The exact discovery capture was 8,192/8,192 live rows, pre/post Excel process
count 0, build 20228/x64/CV2, `Value2`, `NoCache`. The route discovery capture
was 1,024/1,024 IDs and arguments aligned, pre/post process count 0,
`cell_value2_bulk`, `NoCache`, captured at
`2026-08-09T13:21:12.2821502Z`. Generator assertions make both route banks
disjoint from each other and from both exact banks.

## GAUSS composition identified on discovery

The cross-view observations separate wrapper semantics from body arithmetic:

1. GAUSS forms `z = abs(x) * FRAC_1_SQRT_2` and stores the binary64 multiply.
   Native multiply and x87-multiply-then-store are observationally identical on
   the present inputs. Divide and recomputed-square-root forms are refuted.
2. For `abs(x) > 1e-15`, GAUSS publishes through the sign-split complement:
   negative `0.5*Q(z)-0.5`, positive `(1-0.5*Q(z))-0.5`.
3. For `abs(x) <= 1e-15`, GAUSS uses the direct odd small-result route. The
   route-discovery ULP window pins the predicate as inclusive: the binary64
   literal `1e-15`, bits `0x3cd203af9ee75616`, is direct; its immediate
   successor `0x3cd203af9ee75617` is sign-split. The inclusive predicate is the
   nearer publication graph on 1,024/1,024 discovery rows; the strict predicate
   is nearer on 1,022/1,024.
4. Existing ERF and ERFC discovery maps independently reproduce GAUSS on every
   overlap for stored multiply plus sign-split publication: ERF `24/24`, ERFC
   `24/24`. Direct half-ERF is only `21/24`; divide staging is `16/24`.
5. The stable witness is `GAUSS(1) = 0x3fd5d897a241a6fc`. The divide-staged
   alternative publishes `0x3fd5d897a241a6fa` and is refuted.

The route result removes the prior post-epsilon cancellation catastrophe. The
coherent public composite improves from 7,428/8,192 to 7,492/8,192 discovery
rows:

| Subset | Exact | Maximum ULP distance | Sum ULP distance |
|---|---:|---:|---:|
| tiny direct, `abs(x)<=1e-15` | 2,374/2,646 | 2 | 275 |
| branch-190 body | 1,919/1,971 | 8 | 121 |
| public-libm erfc tail | 3,181/3,557 | 2 | 479 |
| saturation | 18/18 | 0 | 0 |

This composite is a diagnostic survivor only; its residuals prevent a
publication or integration gate.

## ERF/ERFC body graph races

### Public small-body families

On 1,508 distinct legacy `0 < z < 0.5` discovery rows:

1. The 18,432 source-backed TOMS-654 branch-190 operation graphs plateau at
   850/1,508 exact, mostly +/-1 ULP and maximum 3 ULP.
2. fdlibm's public small rational scores 558/1,508, maximum 3 ULP.
3. NSWC `erfc1` scores 83/1,508, maximum 7 ULP.
4. Literal public GRATIO complementary-return graphs score 577/1,508 and are
   materially worse than the direct branch-190 form.
5. The distribution-site raw-power graph scores 482/1,508 at this call site.
   Register-continuous x87 sqrt/explog forms remain the best public proxy.

A full 8,192 mixed-spill enumeration of the published `gam1(1/2)` rational
produces 17 distinct Ext80 normalizer values. None hits the empirically inferred
mantissa `0x906eba8214db6c6f`; the nearest public graph is 57 Ext80 mantissa
units away, and substituting every public value does not improve the 850-row
plateau. A 13-site recurrence spill-mask race is flat at the decoded-Q
resolution.

### Symmetric GAUSS inversion of Q

Positive/negative GAUSS pairs uniquely invert the proven wrapper to an internal
Q value without consulting ERF/ERFC answers. The current discovery yields:

- 888 positive/negative pairs in `EPS < x < 0.7`;
- 822 uniquely decoded pairs;
- 784 distinct stored `z,Q` observations;
- public libm `erfc`: 773/784 exact;
- 73,728 source-backed branch-190-plus-publication graphs: 778/784 exact,
  maximum 1 ULP, sum 6 ULP.

All six remaining Q residuals require candidate Q plus one ULP:

```text
0x3fc0000000000001
0x3fc0000000000004
0x3fc0000000000008
0x3fc000000000001d
0x3fc0000000000025
0x3fc6a09e667f3bcd
```

The first five are immediately above `z=1/8`; the sixth is the transported
`sqrt(2)/8` landmark. This is the same localized tooth/comb fingerprint already
measured in the W109 ERF discovery ladders, now isolated before GAUSS
publication. A +/-2,048 Ext80-mantissa scan of the effective normalizer stays
flat at 778/784, so a constant correction is refuted.

### Direct tiny route

Combining the original exact discovery with the direct side of the route bank
gives 3,158 direct-route observations:

1. A rounded binary64 `1/sqrt(2*pi)` constant times `x` scores 2,397/3,158,
   maximum 2 ULP.
2. The best source-backed zero-limit branch-190 association scores 2,632/3,158,
   maximum 2 ULP, sum 537.
3. A +/-4,096 Ext80-mantissa effective-normalizer scan improves only to
   2,638/3,158, maximum 2 ULP, sum 531.

The small-route residual is therefore not removable by selecting one constant
or one published `gam1` mixed-spill result. It remains part of the ERF body
tooth/comb lane.

## Stale hypotheses retired by this checkpoint

The following candidates do not survive discovery:

1. GAUSS as a direct `0.5*erf(x/sqrt(2))` wrapper at ordinary magnitudes.
2. GAUSS input delivery through division by `sqrt(2)` or a recomputed extended
   square root.
3. The distribution raw-power graph reused unchanged at the ERF branch-190
   call site.
4. Literal branch-200/complementary GRATIO return arithmetic for `z<0.5`.
5. fdlibm, Cody/CALERF, NSWC `erfc1`, Boost-era rationals, or host libm as an
   exact small-body identity.
6. A single adjusted normalizer constant as the regular-body or direct-tiny
   last mile.
7. Uniform or per-site binary64 spilling of the public branch-190 recurrence as
   the missing six-row operation graph.

No empirical correction table is admitted as an implementation candidate. The
landmark residuals are retained as discriminators for a coherent arithmetic
graph.

## Reproducibility commands

Run from the OxFunc repository root with the isolated target directory:

```powershell
cargo check --offline --release --manifest-path smart-fuzzer\tools\calc_graph_racer\Cargo.toml --target-dir target-erf-gauss-root --bin race_erf_precise_pow_substrate --bin race_erf_precise_public_small --bin race_gauss_composition --bin generate_gauss_exact_banks
.\target-erf-gauss-root\release\race_gauss_composition.exe . crossview
.\target-erf-gauss-root\release\race_gauss_composition.exe . decode
.\target-erf-gauss-root\release\race_gauss_composition.exe . tiny-route
.\target-erf-gauss-root\release\race_erf_precise_pow_substrate.exe . gauss-q
.\target-erf-gauss-root\release\race_erf_precise_pow_substrate.exe . gauss-route
.\target-erf-gauss-root\release\race_erf_precise_pow_substrate.exe . gauss-route-capture
.\target-erf-gauss-root\release\race_erf_precise_pow_substrate.exe . gauss-composite
```

The combined offline `cargo check` passed. A clean temporary regeneration from
the current generator reproduced all four frozen batch hashes byte-for-byte.

Research-source hashes at this checkpoint:

```text
race_erf_precise_pow_substrate.rs  D1B9BF62481B04785B6D4435C208EBDAD248527FCA0A139254BD83E58D849B94
race_erf_precise_public_small.rs   CE4E9C6D2C0E93CA26A2DEF9F989A6DEF9C0903731A9E70D053ABF34A78699CB
race_gauss_composition.rs          27F1077164874CCBF05DA4831CF5DF14EF61EFF232C74B316DDE792A60FD510A
generate_gauss_exact_banks.rs      A50941F48C5A1E2949201CC3F0F5AD6138A489B6F119B5DCED870C7D57E0AEE9
```

## Gate and status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`

`open_lanes`:

1. Coherent public/source-backed operation graph for the six decoded-Q
   branch-190 residuals and the broader ERF tooth/comb observations.
2. Direct-tiny ERF body graph (520 residual rows remain after the best empirical
   constant scan on the combined corpus).
3. ERFC mid/tail body and boundary graph (public libm remains within 2 ULP but
   is not exact).
4. Exact ERF.PRECISE and ERFC.PRECISE discovery survivors across all numeric
   branches, boundaries, overflow/underflow, and canonical subnormal flush.
5. Frozen exact and route heldout execution; both remain sealed until one
   coherent exact discovery survivor exists.
6. Production, test, formal-model, catalog/map/ledger/bug/workset/bead
   integration, contingent on an exact frozen heldout and root authorization.
7. Alternate Excel application version/channel, compatibility version, and
   locale axes outside the present build-20228/x64/CV2 baseline.
