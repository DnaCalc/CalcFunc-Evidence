# COTH = 1/TANH (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`COTH(x)=1/TANH(x)` 28/28 including `COTH(800)=1` and `COTH(0)=#DIV/0!`.
`COSH/SINH` is 5/9 max 1 ULP. EXP forms are not identities.

TANH is already the worksheet `SINH/COSH` ratio, so COTH is the reciprocal
of that published surface, not the `COSH/SINH` association.
