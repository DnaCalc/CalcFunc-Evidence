# GAMMA odd-eighth recurrence (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject, `A1+k/8` cell-ref
formulas (`k/8` dyadic).

| family | exact n | first miss |
|---|---|---|
| `n+1/8` | 0..=3 | 4.125 (1 ULP) |
| `n+3/8` | 0..=3 | 4.375 (1 ULP) |
| `n+5/8` | 0..=2 | 3.625 (1 ULP) |
| `n+7/8` | 0 only | 1.875 (1 ULP) |

Seeds: `1/8=0x401e22c196233d23`, `3/8=0x4002f6a73f0a9838`,
`5/8=0x3ff6f3ca0920b668`, `7/8=0x3ff16f374f724016`.

Landed those finite n ranges only. G3-02 remains open.
