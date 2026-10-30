# GAMMA half-integer recurrence `16.5..=19.5` (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject, cell-ref formulas.

Closed form `(2n-1)!! / 2^n * GAMMA(0.5)` with seed `0x3ffc5bf891b4ef6b`
matches `GAMMA(n+0.5)` for `n=0..=15`. At `16.5` that closed form diverges
from Excel; the native recurrence from the closed-form `15.5` value matches:

| x | Excel bits | `(x-1)*GAMMA(x-1)` |
|---|---|---|
| 16.5 | `0x4292e1900e84c080` | exact |
| 17.5 | `0x42d3789c8ef8e684` | exact |
| 18.5 | `0x43154beb3c603c20` | exact |
| 19.5 | `0x43589fc7fdcf4585` | exact |
| 20.5 | `0x439e02bbbd549cbb` | 1 ULP (`…cba`) |

Landed `16.5..=19.5` only. `n>=20.5` remains open. G3-02 remains open.
