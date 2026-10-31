# Excel versus the 15 vendor-dependent x87 hardware results

2026-10-31. All 15 fresh Excel answers match the frozen AMD hardware result
exactly: 13 LN inputs, one EXP and one COS. All differ by one ULP from the
recorded Intel hardware result. This measures Excel on AMD only; Excel on Intel
has not been measured here. These selected differences do not establish a
general algorithm for Excel's LN/EXP/COS.

`hardware-frozen.json` fixed all 15 AMD/Intel hardware predictions before the
first new Excel reading. `x87-source.rs` retains the exact source bytes it hashes.
The source is DnaCalc 1e636dde677b26d53367a31731b2a0fe0b2aad32,
crates/calc-func/tests/f1_support/x87_cpu.rs. The existing witness reader then
calculated and synced each function's CalcFunc prediction file before its Excel
capture. Both the hardware freeze and those model freezes remain labelled as
predictions, separate from Excel's measured expected_bits.

Readings: readings/excel-20527/LN.json, EXP.json and COS.json. Each row retains
its frozen CalcFunc output; each capture retains its build/platform/CPU and
SHA-256 links to the inputs and prediction files copied here. Native Fast at
the same DnaCalc commit matches all 15 readings; CalcFunc source was unchanged.
Zero inputs changed, zero rows were unread, and zero were skipped.

Excel 16.0 build 20527, file 16.0.20527.20088, Windows x64
(NT 10.0.26200.0), AMD Ryzen 7 4800H with Radeon Graphics. Values were written
and read as binary64 through Value2 in blank workbooks. AutomationSecurity was
read as 1 before and after each capture. No Trust Center, security or registry
setting changed; only the owned Excel processes were stopped. Raw requests and
worker results are retained. Initial input-format/CLI preflights started no Excel.

Validation: all input/frozen-file hashes checked; all 15 exact bit comparisons
checked against both vendor columns; archive-evidence.py verify --sample 100
passes. No coefficients or numerical kernels changed. DnaCalc dc-ymjf.5 owns
independent readings; the numerical lane retains general parity work.
