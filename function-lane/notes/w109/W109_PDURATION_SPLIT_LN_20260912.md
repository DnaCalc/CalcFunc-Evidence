# PDURATION split worksheet-LN graph (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject, cell-ref `PDURATION`.

Excel's PDURATION is

`(LN(fv) - LN(pv)) / LN(1+rate)`

with the identified worksheet LN (`excel_log`), **not** `LN(fv/pv)/LN(1+rate)`.

On an 80-row mixed grid: split LN 80/80; fused-ratio LN and production CRT
`.ln()` 20/80 max 17 ULP. Native subtract/divide of the two worksheet LNs
agrees with x87 restages on this grid; land the native split.

Pins: `PDURATION(0.025,2000,2200)=0x400ee10182bb35e8`,
`PDURATION(0.04,999,1234)=0x40158bc055fd3ec8`,
`PDURATION(0.03,12000,15000)=0x401e3251e38ae145`.
