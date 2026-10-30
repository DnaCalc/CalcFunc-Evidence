# GAMMALN = LN(GAMMA) at selected (0,1) seeds (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`GAMMALN(x)=LN(GAMMA(x))` is exact at `x=1/2` (already), `1/5`, `1/3`,
and `1/7`. Other landed GAMMA seeds are 1–13 ULP from that composition
(`1/4` 1 ULP, `3/4` 8 ULP, `4/5` 13 ULP).

Production routes those three arguments through `excel_log(gamma_kernel(x))`.
Not a general composition.
