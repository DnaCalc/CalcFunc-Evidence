# SEC = 1/COS and CSC = 1/SIN (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`SEC(x)=1/COS(x)` 8/8 and `CSC(x)=1/SIN(x)` 8/8. Production already uses
the x87 reciprocal of `excel_cos` / `excel_sin`. Pins of the live 20326
bits.
