# COSH = (EXP(x)+EXP(-x))/2 (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`COSH(x)=(EXP(x)+EXP(-x))/2` 40/40 on a signed grid from `0` through `100`,
including tiny (`1e-8`) and negatives. Spilled `EXP` cells `(E+Em)/2`,
`E/2+Em/2`, and `0.5*E+0.5*Em` are the same 40/40 on this grid.

libm `cosh` is 1 ULP off Excel at `0.001`, `0.01`, and `10`.

`SECH(x)=1/COSH(x)` 40/40 on the same grid, so SECH follows the COSH kernel.

`SINH` is not this EXP pair: fused `(EXP-EXP(-))/2` is 27/40 (misses `|x|<~0.25`
except `0.2`; `0.25`/`0.3` are 1 ULP). Cubic `x+x^3/6` only covers `|x|<=1e-4`.
Not landed.

`TANH` vs worksheet `SINH/COSH` is 35/40 on this wider grid (misses `0.001`,
`0.01`, `0.4` and sign mirrors). The earlier 8/8 identity remains for that
smaller pin set; it is not a universal last-bit identity.
