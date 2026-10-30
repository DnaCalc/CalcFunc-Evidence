# COT = 1/TAN (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`COT(x)=1/TAN(x)` 10/10 on a signed grid. `TAN` vs `SIN/COS` is 3/10
max 1 ULP, so COT is the reciprocal of the published TAN surface, not
`COS/SIN`.

Production already uses the x87 reciprocal of `excel_tan`. Pins of the
live 20326 bits.
