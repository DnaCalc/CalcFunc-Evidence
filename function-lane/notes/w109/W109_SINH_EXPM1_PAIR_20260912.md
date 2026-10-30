# SINH = (expm1(x)-expm1(-x))/2 (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

Worksheet `(EXP(x)-EXP(-x))/2` is only 27/40 (misses `|x|<~0.25` except
`0.2`; `0.25`/`0.3` are 1 ULP). Cubic `x+x^3/6` only covers `|x|<=1e-4`.
Quint/deg7/horner are not identities.

Excel's internal Kahan `expm1` (already identified for EXPON/GAMMA.DIST a=1)
gives `SINH(x)=(expm1(x)-expm1(-x))/2` on **37/37** live bits from `0` through
`20` including the EXP-pair misses (`0.001`, `0.01`, `0.25`, `0.3`) and
negatives. libm `sinh` is 1 ULP off at `0.01` and `2`.

`CSCH` follows `1/SINH`.

`TANH` vs worksheet `SINH/COSH` remains 35/40 on the wider COSH grid — not a
universal last-bit identity. The earlier 8/8 pin set still holds.
