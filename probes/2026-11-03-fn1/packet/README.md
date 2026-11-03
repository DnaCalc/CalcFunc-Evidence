# Functions lane fn1 Excel questions

Unanswered calls, 2026-11-03. No expected answer is supplied. Keep these files and their hashes unchanged; retain raw results, input read-back, Excel build, locale and calculation settings. Predictions are not answers.

Numeric arguments are fixed binary64 `0x` bit strings, as the reader requires; logical and text arguments keep their types.

The scalar files use the research lane’s standard `function` / `witnesses` / `id` / `args` input schema consumed by `cargo xtask witness read --inputs` (the reader used for R16/R18). The R16/R18 packet directories are not available in this Linux checkout; compatibility is based on the committed reader. It freezes actual product predictions before asking Excel. A missing function should remain a missing-function prediction. Do not use `--new-only`: these include controls already measured elsewhere.

Run each function separately on the Windows lane, for example:

```powershell
cargo xtask witness read --func EUROCONVERT --inputs <packet-dir>/EUROCONVERT.inputs.json
cargo xtask witness read --func MATCH --inputs <packet-dir>/MATCH.inputs.json
```

Repeat for each `*.inputs.json`; the function is the filename before `.inputs.json`. Do not change Office language, security or registry settings. EUROCONVERT may require the Excel Euro Currency Tools add-in: first retain the default availability result; if explicitly loaded for measurement, record that fact and keep the two contexts apart. JIS is a regional spelling: prior English Excel probes returned #NAME?; measure it without presuming it aliases DBCS. ECMA.CEILING has file-form metadata but no verified value.

`sheet-fn1_collation.txt` contains formula questions. Add it as its own section to the existing `crates/calc-func/tests/fixtures/make-catalogue-fixtures.ps1` / catalogue oracle, regenerate and run `cargo xtask capture --pending`. This reuses the single workbook and section lineage. The formulas use UTF-8 non-ASCII literals; preserve the file encoding when reading them. Do not create another capture harness. Add MATCH/XMATCH array and SORT/SORTBY cases to that same section after scalar intake identifies the comparison rule.

The nine current corpus text failures are number-to-text ties already under the research lane’s R18 CONCAT packet. The four type/error failures are Bessel/LOGEST numerical cases owned there; this packet does not duplicate those studies. The two GETPIVOTDATA refusals need pivot context, owned by dc-8wp. The baseline’s four collation refusals are addressed by the comparison grid above. A bounded primary-prefix change now computes one of those four; the unknown iteration weights still need measurement.
