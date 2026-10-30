# ERFC implied-F inverse-problem campaign

Date: 2026-08-31
Lane: W109. Host: `dna-firehorse` (12/16 vCPU).
Does not land kernels. Heldouts unnamed.

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`
- `open_lanes`: ERFC.PRECISE F-body (ERF/GAUSS/NORMSDIST inherit)

## Local explorer (same day, before the long cubes)

Bin: `race_erfc_f_explore`. Oracle `F_or = Q / excel_exp(-RN53(RN64(z·z)))`.

NSWC mid residual on 7741 rows:

| ULP | count |
|---|---|
| 0 | 2389 |
| 1 | 3414 |
| 2 | 1453 |
| 3 | 398 |
| 4 | 73 |
| 5 | 11 |
| 6 | 2 |
| 7 | 1 |

75% of mid is ≤1 ULP. The "7 ULP ceiling" is one row, not a wall.
Sign switches 2142 — oscillatory last-bit comb, not a wrong family.

Truncated CF (tail exact plateaus at **n=21**, 1283/5934). Short n=8 is 636.
Published NSWC bilinear t is locked: other t-maps dump every row over the ULP cap.

Piecewise `NSWC(z<cut) else CF-as714-n80` best at **cut=1.6**, all-exact **3699**
(mid 2416 + tail 1283) vs NSWC-all 3632. Constraint, not an identity.
CDFLIB `erfc1` loses mid (704) but is the closest named pin at z=1.875 (1 ULP)
and z=5 (3 ULP).

## Firehorse cubes

Bin: `campaign_erfc_fbody`. Out dir:
`/data/projects/DnaCalc/OxFunc/smart-fuzzer/work/w109/erfc-fbody-campaign/`

x87 store-after-step masks on truncated CF (the only large discrete tree
that is still live). Native f64 already stores every op, so native masks
are skipped.

| axis | space | note |
|---|---|---|
| CF/gaut/n12b2, CF/as714/n12b2 | 2^24 | 2 bits/step (div+add) |
| CF/{gaut,as714}/n16 | 2^16 | 1 bit/step |
| n20, n21, n24 | 2^n | 1 bit/step |

R0 on the host writes named F + piecewise before the cubes.
Bar: mid 2389, tail 1283. HIT_MID / HIT_TAIL are discovery alerts.

```text
MAX_HOURS=96 RAYON_NUM_THREADS=12 ./run-erfc-fbody-campaign.sh
```

Stop: `touch STOP` in the out dir. Resume: same command (progress keys skipped).
Monitor: `scp dna-firehorse:.../erfc-fbody-campaign/STATUS.md .`

GitHub copy at cube/phase gates: `docs/function-lane/w109-erfc-fbody-campaign/`
once that snapshot dir is created. `smart-fuzzer/work/` is gitignored.

Complementary Lentz recurrence (same host, leftover 4 vCPU): see
[`W109_ERFC_FSWEEP_20260831.md`](W109_ERFC_FSWEEP_20260831.md). Do not stop
this 12-thread backward-CF campaign to make room; the Lentz launcher is
sized for the spare cores.
