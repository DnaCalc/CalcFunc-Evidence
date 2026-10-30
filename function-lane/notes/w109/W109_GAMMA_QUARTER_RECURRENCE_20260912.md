# GAMMA quarter-integer recurrence `n+1/4` and `n+3/4` (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject, `A1+1/4` / `A1+3/4`
cell-ref formulas (0.25 and 0.75 are dyadic).

Native recurrence from seeds is bit-exact for `n=0..=5`; first miss at
`6.25` / `6.75` (1 ULP vs recurrence).

| x | Excel bits |
|---|---|
| 0.25 | `0x400d013fc47eeeec` |
| 1.25 | `0x3fed013fc47eeeec` |
| 2.25 | `0x3ff220c7dacf5554` |
| 3.25 | `0x400464e0d6293ffe` |
| 4.25 | `0x402091f6ae0183fe` |
| 5.25 | `0x40419b1618e19c3e` |
| 0.75 | `0x3ff39b4e8b50f62d` |
| 1.75 | `0x3fed68f5d0f97144` |
| 2.75 | `0x3ff9bbd716da431c` |
| 3.75 | `0x4011b123dfb60e23` |
| 4.75 | `0x40309611a1baad41` |
| 5.75 | `0x4053b234f00dadbd` |

Landed `n=0..=5` only. G3-02 remains open.
