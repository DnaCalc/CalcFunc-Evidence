# GAMMALN Stirling x>=8 — worksheet LN + x87 DR q

Date: 2026-09-12
Lane: W109 G3-02. High-band kernel only. G3-02 remains open.

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`
- `open_lanes`: two 1-ULP Stirling rows; B1 `[0.7,1.5)` coefficients; B2 leftover;
  GAMMA composition; G3-01 fractional-a inheritor

## Graph

```text
ln   = LN87(x)                         # worksheet FYL2X, stored binary64
q1   = DR((x - 0.5) * ln)              # x87 PC64 then binary64 store
q2   = DR(q1 - x)
q    = DR(q2 + LS2PI)
z    = 1/x                             # native
y    = z*z                             # native
w    = fdlibm w6..w1 Horner in y       # native
out  = DR(q + z*w)
```

`LS2PI = 0x3fed67f1c864beb5`. This is the 2026-08-09 reconstructed high-band
graph, now in `excel_numeric::gammaln::stirl8`.

## Evidence

| Replay | Exact | Max \|ULP\| |
|---|---:|---:|
| Prior production (native `ln`, native q) | 1701/1711 | 2 |
| LN87, native q | 1707/1711 | 2 |
| LN87, DR q, native out | 1708/1711 | 1 |
| LN87, DR q, DR out (landed) | 1709/1711 | 1 |

Union: unique `x>=8` rows from current-build discovery, `answers-gammaln.json`,
`answers-dense1.json`, `answers-L-round3.json`, `answers-r0.json`,
`answers-r2.json`, `answers-validate.json`.

The only remaining misses are the two 2026-08-09 rows:

| ID | Input | Excel | OxFunc | ULP |
|---|---|---|---|---:|
| old-resid-02 | `0x40215bf4d43f4d44` | `0x4023d98694477879` | `0x4023d98694477878` | -1 |
| old-resid-03 | `0x40234ce3244e3245` | `0x40280a8dd6771c9a` | `0x40280a8dd6771c99` | -1 |

Live Excel 16.0 build 20326 / CV2 / Value2 (2026-09-12) republishes the same
four pin bit-patterns as the 20228 discovery bank (`old-resid-00/08` now exact;
`02/03` still Excel's bits above). GAMMALN and GAMMALN.PRECISE agree.

This is not a function-phase-complete claim. The two 1-ULP rows sit between
adjacent stored-log effects (bounded-negative 2026-08-09). B1/B2 and GAMMA
composition stay open.

## GAMMA integer slice (same session)

Live Excel 16.0 build 20326: `GAMMA(n)` for positive integers `n=1..=88` is
the reverse native product `(n-1)*(n-2)*...*2` (empty product 1 for `n=1,2`).
The forward product diverges at `n=26`. Reverse first miss is `n=89`.
`GAMMA(172)` remains `#NUM!`. Non-integers and `n>=89` stay on the open
lgamma/exp kernel. Landed in `gamma_kernel`; G3-02 remains open.
