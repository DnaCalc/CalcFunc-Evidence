# GAMMA selected x in (-1,0) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

Worksheet `GAMMA(x)=GAMMA(x+1)/x` is exact on 8/12 of a first grid and
12/28 of a second grid. IEEE complement-seed division is not the graph:
`1+(-1/3)` is not `2/3`, so `GAMMA(2/3)/(-1/3)` is 1 ULP from published
`GAMMA(-1/3)` even when `GAMMA(2/3)` is the Excel seed.

Landed as published-bit seeds (not a general peel). Misses of 1 ULP
(`-3/4`, other fifths, most sevenths/ninths/tenths/twelfths/sixteenths)
are not claimed.

Exact slice includes `-1/3,-2/3,-1/4,-1/5`, odd eighths, `-5/7,-6/7`,
`-2/9,-7/9`, `-7/10`, `-5/12,-7/12`, and `-1/16,-5/16,-7/16,-9/16,-15/16`.
