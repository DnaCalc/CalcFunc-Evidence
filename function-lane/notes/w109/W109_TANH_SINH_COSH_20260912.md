# TANH = SINH/COSH (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`TANH(x)=SINH(x)/COSH(x)` 8/8 on a signed grid. The EXP form
`(EXP(2x)-1)/(EXP(2x)+1)` is 5/8.

libm `tanh` is 1 ULP off `TANH(0.5)`. Production now uses the worksheet
`SINH/COSH` ratio.
