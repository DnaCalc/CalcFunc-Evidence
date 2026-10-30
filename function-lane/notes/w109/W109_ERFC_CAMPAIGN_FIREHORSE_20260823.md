# ERFC-body firehorse campaign

Date: 2026-08-23
Host: `dna-firehorse` (16-vCPU AMD EPYC KVM, x87 last-bit matched this
Windows AMD box 3157/3157)
Lane: W109 ERFC.PRECISE body — store-site × arithmetic × staging tree

## Status axes

- `execution_state`: `in_progress` (R1m exhausted; finishing `R1/z0/r0` then
  `--only R4,R2`; remaining R1/R1p skipped; F-form pivot after that)
- GitHub snapshot (coordination/backup):
  [`w109-erfc-campaign/`](w109-erfc-campaign/) — copy STATUS, REGION_MAP,
  checkpoint, leaders, pin-hits from firehorse at each cube/phase gate and
  push. `smart-fuzzer/work/` is gitignored.
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`
- `open_lanes`: ERFC body; this campaign does not land kernels

Heldouts are not named and are not copied. Discovery banks only.

## Why this campaign

Named public F graphs (NSWC, Cody, SLATEC Chebyshev) and a 5-axis
association race peaked at 6127/15556 (mid 3332/7741), pins still 2–4 ULP.
The leftover is *where* Excel stores in a double-precision F-body around
unsplit `excel_exp(−z²)`. Firehorse can legally run `excel_exp` against
the AMD Excel banks.

A local smoke showed ~900 configs/s on 8 threads, so a 16-bit cube
finishes in minutes and would idle the machine. The long run is a
**26-bit** P/Q/R + t-formation store mask on x87-continuous Horner
(~67 million configs per axis, about half a day to a day per axis at
12 threads). Native and every-op/all-stage spill ignore extra mask
bits, so they are scored once (R1base). Ratio includes `u*(1/v)`.
NSWC mid_cut 1.5 (the assoc-race winner) is first in the queue.

## CPU / time

- 12 of 16 vCPUs (75%, under the ~80% cap), `RAYON_NUM_THREADS=12`
- default `--max-hours 96` (4 days); stop early with a `STOP` file
- restart = same command; completed chunks are skipped
- if every named cube finishes early, the process **exits** rather than
  re-rolling the already-enumerated 16-bit space

## Tree regions (explored in order)

| ID | Region | What is enumerated | Completeness |
|---|---|---|---|
| R0 | named F + implied-F pins | libm, production, NSWC DERFC0 native, Cody-unsplit, assoc-race bar cfg, F = Q/exp(−z²) vs NSWC/Cody at five pins | exhaustive, minutes |
| R0c | NSWC P/Q/R ±1 ULP | one-coefficient next_up/next_down on the published decimals (Cody last-bit already noise) | exhaustive, minutes |
| R1base | mask-insensitive arith | Native / EveryOp53 / Pc53 / all-stage-spill × zz × uv × mid_cut {4, 1.5} | exhaustive, minutes |
| R1m | NSWC 26-bit P/Q/R + t-formation store mask × zz {x87-DR first, native} × uv {store first, continuous, recip}, mid_cut=1.5 | PQR below 1.5, AA/BB above. First axis is the assoc-race bar. ~67e6 configs/axis | first, then the other five R1m axes |
| R1 | same 26-bit mask, mid_cut=4 | PQR on the whole mid band `[0.5,4)` | after R1m, if wall-clock remains |
| R4 | NSWC AA/BB 19-bit (AA 0–7, BB 8–18) × zz × uv, mid_cut=1.5 | PQR continuous below 1.5 | after R1 |
| R2 | Cody C/D 16-bit × zz × uv | SPECFUN CALERF, X87Cont | after R4 |
| R1p | one Pc53 26-bit PQR+t cube | zz-DR + store uv + mid_cut 1.5, if wall-clock remains | last |

`REGION_MAP.md` always says which cube and which mask prefix have been
finished. Scoring is the 7,741-row mid band `[0.5, 4)` plus pin hits.
All-band R0 is recorded separately. The assoc-race mid bar (3332/7741)
is printed on every STATUS snapshot.

## Checkpoints

Directory: `smart-fuzzer/work/w109/erfc-campaign/`

| File | Role |
|---|---|
| `STATUS.md` | human snapshot, rewritten after every chunk (~4096 configs) |
| `R0.md` `R0c.md` `R1base.md` | phase reports that STATUS extra would otherwise overwrite |
| `REGION_MAP.md` | named tree regions and per-axis next-mask |
| `status.json` | same numbers, machine-readable |
| `checkpoint.json` | completed chunk ids; resume source |
| `leaders.jsonl` | every config that beats running best exact/mid/pins |
| `MONITOR.md` | scp/ssh recipes (copied into the out dir) |
| `campaign.log` | stdout/stderr from the tmux session |
| `HIT_ALL_MID` | written only if some config is exact on all mid rows |
| `HIT_PIN` | written if a pin z goes exact |

`STOP` file in that directory: finish the current chunk, write checkpoint, exit.

## Monitor from this PC

```text
scp dna-firehorse:/data/projects/DnaCalc/OxFunc/smart-fuzzer/work/w109/erfc-campaign/STATUS.md .
scp dna-firehorse:/data/projects/DnaCalc/OxFunc/smart-fuzzer/work/w109/erfc-campaign/REGION_MAP.md .
ssh dna-firehorse -- tmux ls
ssh dna-firehorse -- tmux capture-pane -t oxfunc-erfc-campaign -p | tail
```

A few-hour look-in is useful: R0/R0c/R1base finish in minutes and then
STATUS shows the first R1 mask prefixes. A multi-day look-in is the
full named cubes plus leaders.jsonl.

## Session

tmux session `oxfunc-erfc-campaign` (detached). Reattach:
`ssh -t dna-firehorse tmux attach -t oxfunc-erfc-campaign`
Detach: `Ctrl-b d`. Survives SSH drop. Reboot would kill it.

A same-command resume after the 96h cap is a **no-op**: `started_unix` is
frozen in `checkpoint.json`, so `timed_out` stays true at `--max-hours 96`.
To continue remaining cubes, raise the cap (`MAX_HOURS=300` on 2026-08-30).
Completed progress keys are still skipped.

## 96-hour cap outcome (exited 2026-08-27 15:49 UTC)

Recorded 2026-08-30 from the firehorse out dir. Snapshot copy:
`smart-fuzzer/work/w109/erfc-campaign-96h-cap-20260827/` (gitignored).

| | |
|---|---|
| wall clock | 96.00 / 96 |
| configs | 432,595,042 |
| HIT_ALL_MID / HIT_PIN | none |
| best mid | **3336**/7741 max_ulp=7  `R1m/z0/r0 /mask=0048000` |
| named mid bar | 3332/7741 `nswc_x87cont_zzdr_store_mid15` |
| best all-band | 6005 `nswc_x87cont_zzdr_store_mid15` |
| pins exact on leader | 0 (`best_pins=1` is the R0c fluke `R0c/R[1]/up` at 2850/7741) |

Finished cubes: R0, R0c, R1base, and **all six** R1m 26-bit PQR+t axes
(mid_cut=1.5 × zz_dr × {uvS,uvC,uvR}). The only masks that beat the bar
appeared in the first minutes of `R1m/z0/r0`:

| mask | bits | mid exact |
|---|---|---|
| `0x0020000` | bit 17, R Horner stage 3 | 3335 |
| `0x0048000` | bits 15+18, R Horner stages 1 and 4 | **3336** |

That is a **+4 row** store-site wiggle on the same 7 ULP ceiling, not a
body. Exhausting the other five R1m cubes did not move the scoreboard.
Do not land.

Left at cap, still in the queue:

| id | next at cap | note |
|---|---|---|
| R1/z0/r0 | 0x1c8e000 / 0x4000000 (~44.6%) | PQR on `[0.5,4)`, zz_dr uvS |
| R1/z0/r1 … R1/z1/r2 | 0 | five untouched 26-bit cubes |
| R4/* | 0 | six 19-bit AA/BB cubes |
| R2/* | 0 | six 16-bit Cody cubes |
| R1p/mid15 | 0 | one Pc53 26-bit cube |

At the observed ~4.5e6 configs/h, the leftover is about 98 wall hours.
2026-08-30 resume uses `MAX_HOURS=300` (~124 h remaining from then) so
the leftover cubes can actually run. The process was not running after
the cap; tmux session `oxfunc-erfc-campaign` had exited.

## 2026-08-31 redirect: finish `R1/z0/r0`, then R4+R2 only

R1m (all six 26-bit mid_cut=1.5 axes) is exhausted: +4 mid rows, still 7 ULP,
0 pin identities. Remaining R1 26-bit cubes are the same PQR F on a worse
cut. After the in-flight `R1/z0/r0` cube finishes, skip the other five R1
axes and R1p. Run:

```text
ONLY=R4,R2,R0aabb MAX_HOURS=300 ./run-erfc-campaign.sh
```

`--only` is a prefix filter (`R4` → all `R4/…` jobs). Then pivot off
NSWC PQR store-masks: AA/BB±E last-bit poke, then F-form race against
implied `Q/excel_exp(−z²)`.

GitHub is the coordination/backup copy. At each cube or phase gate, copy
the firehorse files into
[`docs/function-lane/w109-erfc-campaign/`](w109-erfc-campaign/) and push.
Do not rely on `smart-fuzzer/work/` (gitignored).
Helper: `smart-fuzzer/tools/calc_graph_racer/snapshot-erfc-campaign.ps1`.

### `R1/z0/r0` finished 2026-08-31 ~09:15 UTC

Cube done (`0x4000000`). Scoreboard **unchanged**: 3336/7741 max 7 ULP,
0 HIT_PIN / HIT_ALL_MID. The process had already opened `R1/z0/r1` at
`0x000f000` (61,440 configs); STOP aborted that axis. Remaining R1 and
R1p are skipped. Next process: `ONLY=R4,R2,R0aabb MAX_HOURS=300`.

### R4 + R2 + R0aabb finished 2026-08-31 ~10:02 UTC

`exit-regions`. 473,432,210 configs. Scoreboard **unchanged**:

| | |
|---|---|
| best mid | **3336**/7741 max 7 ULP `R1m/z0/r0 mask=0048000` |
| HIT_ALL_MID / HIT_PIN | none |
| new leaders.jsonl lines | none |

All six R4 AA/BB 19-bit cubes and all six R2 Cody 16-bit cubes finished.
R0aabb (48 native ±1 ULP pokes of AA/BB/E) peaked at **2924**/7741
(`E[2]/up`), still 7 ULP, 0 pins. That is last-bit noise on the native
graph, not a stored-decimal hit.

**NSWC/Cody store-site and last-bit on this F are exhausted.** Do not
resume leftover R1 or R1p. Pivot: implied-F form race
`F = Q / excel_exp(−z²)` against other public rationals.

## Binary

`smart-fuzzer/tools/calc_graph_racer` bin `campaign_erfc_body`

```text
cargo run --release --bin campaign_erfc_body -- \
  --dir ../../work/w109/G3-01-dist \
  --out ../../work/w109/erfc-campaign \
  --threads 12 --max-hours 96 \
  --only R4,R2
```

`ONLY=R4,R2` is the env form used by `run-erfc-campaign.sh`. The script
always rebuilds so a pulled `--only` binary is what runs.
