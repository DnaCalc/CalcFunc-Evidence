# Independent Excel readings: CalcVba integration run 2

Captured 2026-10-31 on Excel 16.0 build 20527, file version 16.0.20527.20088,
64-bit Windows (OS reports NT 10.0.26200.0), AMD Ryzen 7 4800H with Radeon Graphics.
Each reading file carries that environment. Values were calculated in a new blank
workbook through the existing calc-oracle-excel bulk Value2 reader, not file caches.
No Trust Center, macro-security or registry setting was changed. AutomationSecurity
was read as 1 before and after each run. Owned Excel PIDs 19592 and 16148 stopped;
the pre-existing PID 3144, started 2026-10-30, remained running.

Frozen model: DnaCalc 379d51f9f753d5d9874520bbffc838f1cbca19aa, native Fast, unchanged
CalcFunc sources. The frozen files were synced before Excel started. Their SHA-256
and the exact input SHA-256 are in each reading's capture_provenance. The local
.gitattributes preserves JSON bytes across checkouts so these hashes remain valid.
The retained_frozen_file and retained_inputs_file paths are relative to this repo.

| Scope | Exact matches / total | Failed | Worst distance |
|---|---:|---:|---:|
| New ERF.PRECISE, abs(x)<0.01 | 3908 / 4096 | 188 | 3 ULP |
| Uniform ERF subset | 2887 / 3072 | 185 | 3 ULP |
| Logarithmic ERF subset | 1021 / 1024 | 3 | 1 ULP |
| GAMMA changed recorded inputs | 2 / 97 | 95 | 1167 ULP |
| New GAMMA adjacent inputs | 4 / 194 | 190 | 880 ULP |

There were zero unread, missing or changed inputs in either capture. Match means
bit equality, not a tolerance. ERF misses: 165 at 1 ULP, 22 at 2 ULP, one at 3 ULP.
The 4096 ERF inputs were selected with Python Random seed 20261031: 3072 uniform
on (-0.01,0.01), 1024 logarithmic magnitudes from 2^-40 to 0.01 with random signs.
All were excluded against 614341 distinct inputs (1024747 rows, 51 bank files)
before asking Excel. A recorded-row control was refused before prediction/startup.
This is the first independent test of this fitted small-x model in this run.

GAMMA's 97 controls are rechecks of known fitted inputs, not independent inputs.
They were selected by replaying df1215e's parent with the same CalcFunc and verdict
helpers: 12312 rows, 437 prior matches, 439 fitted matches, exactly 97 changed.
All 97 fresh Excel values agree with the recorded answers. The prior model matched
0/97 and the fitted model 2/97 on these controls. The 194 adjacent binary64 inputs
were absent from the loaded GAMMA banks and were selected before fresh readings.
They give 4/194 matches; this does not identify Excel's general GAMMA algorithm.

This reading work changed no coefficients or numerical kernels. The concurrent
statistical-function lane retired the fitted GAMMA coefficient change in DnaCalc
17e42ce; these measurements retain the explicitly frozen 379d51f/df1215e model. The answers are under
readings/excel-20527/; each row keeps the frozen calc_func_prediction beside
Excel's actual expected_bits. This directory retains inputs, frozen predictions,
raw worker requests/results and a machine-readable summary. An initial preflight
failed PowerShell parsing before any Excel PID; the column-reader syntax was
corrected and tested in Windows PowerShell before these two successful captures.
