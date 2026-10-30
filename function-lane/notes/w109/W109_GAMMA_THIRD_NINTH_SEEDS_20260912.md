# GAMMA thirds and ninths in (0,1) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

Thirds seeds. `GAMMA(1/3)` is 6 ULP from the generic path. The n+1/3
recurrence was previously 7/21 and is not claimed.

| x | GAMMA bits |
|---|---|
| 1/3 | `0x40056e77539482f2` |
| 2/3 | `0x3ff5aa77928c3679` |

Ninths that are not thirds:

| x | GAMMA bits |
|---|---|
| 1/9 | `0x40210b9dc79fe8d4` |
| 2/9 | `0x40106d2331a5de8d` |
| 4/9 | `0x3fffe2e4518a6b60` |
| 5/9 | `0x3ff99c88812c4a39` |
| 7/9 | `0x3ff30adbf89161c8` |
| 8/9 | `0x3ff13e800bd48928` |

Seeds only; recurrence not claimed.
