# Blind Excel readings for dna-firehorse round 3

541 rows requested on 2026-10-31: PMT 132, GAMMA.DIST 128, BINOM.DIST 120,
POISSON.DIST 161. The frozen request packets were copied byte for byte from
codex-runs/fresh-questions-r3. Their hashes are in blind-manifest.json.
No prediction file was opened or scored before the answer commit.
These are targeted questions (537 new argument identities and four rechecks),
not an unbiased pass-rate sample. Missing historical worker handover files named
by REPRODUCTION.txt were absent from the supplied request bundle; its available
REPRODUCTION.txt and GAMMA fresh-independent-plan/HANDOVER.md were read.

The unchanged DnaCalc b952767 calc-oracle-excel witness-worker/1 reads typed
binary64/logical inputs through bulk Value2, then verifies their readback.
The existing run_isolated supervisor owns each worker and reported Excel handle.
Each packet retains its raw request, result and isolation record. reader/ retains
one exact copy of the shared worker scripts. The launcher calls run_isolated directly; no new capture adapter or
formula/value conversion path was added to DnaCalc. launcher.rs is the source;
its dependency is the existing calc-oracle-excel package in DnaCalc-cfml.
For replay, copy reader/*.ps1 into a fresh packet directory beside request.json,
then run the launcher with that directory as its only argument.

Environment: Excel 16.0 build 20527, file 16.0.20527.20088, x64;
Windows NT 10.0.26200.0; AMD Ryzen 7 4800H with Radeon Graphics.
AutomationSecurity read 1 before and after every capture. No Trust Center,
macro-security or registry setting changed. All four owned Excel processes
exited normally; the pre-existing owner PID 3144 was left running.
Two launcher preflights failed on PowerShell extended-path parsing before
starting Excel. They supplied no answers.

Standard witness-reading files are readings/excel-20527/*-calcvba4.json.
537 rows have valid answers with unchanged inputs; none were skipped.
Four POISSON.DIST means (000ffffffffffffc through 000fffffffffffff) changed
when written through Value2. Those raw results are retained but are not answers
to the requested tuples; they remain unread failures in prediction scoring.
Recheck: python probes/2026-10-31-calcvba-run4/verify-blind.py.
Repository check: python archive-evidence.py verify --sample 100 --seed 4.
Frozen prediction scores are deliberately absent from this first answer commit.

## Frozen prediction scores (opened after answer commit 0df452ec)

| Function / frozen model | Exact matches / all questions | Failed | Worst numeric ULP |
|---|---:|---:|---:|
| PMT current application, native and software | 78 / 132 | 54 | 3 |
| PMT pre-identity, native and software | 15 / 132 | 117 | 4,627,045 |
| GAMMA.DIST retained candidate A | 34 / 128 | 94 | 5 |
| GAMMA.DIST baseline | 0 / 128 | 128 | 31 |
| GAMMA.DIST research B (unretained) | 34 / 128 | 94 | 5 |
| GAMMA.DIST mathematical rounded reference | 6 / 128 | 122 | 62 |
| BINOM.DIST baseline (retained product) | 25 / 120 | 95 | 57 |
| BINOM.DIST tiny compensated (unretained) | 5 / 120 | 115 | 60 |
| BINOM.DIST tiny control (unretained) | 5 / 120 | 115 | 61 |
| POISSON.DIST retained tiny endpoint | 31 / 161 | 130 | 75,996 |
| POISSON.DIST baseline | 28 / 161 | 133 | 75,996 |
| POISSON.DIST research u_scalar | 31 / 161 | 130 | 76,911 |
| POISSON.DIST research u_pc64 | 29 / 161 | 132 | 75,996 |

POISSON failures include all four changed-input rows; its four recorded-input
rechecks remain in the denominator (one matches tiny endpoint). Its 157 new
argument identities therefore give 30 matches, 123 mismatches and four unread.
PMT gains 63, A gains 34 and tiny endpoint gains three against their respective
baselines, with no exact-match losses in these selected questions. PMT's four
overflow questions all match; its remaining failures include four numeric
predictions where Excel returned #NUM!, 47 one-ULP and three three-ULP misses.
Numeric ULP maxima exclude error/number differences, which still count as fail.
These targeted results do not identify a general Excel algorithm or establish
full-function parity. No coefficient, numerical kernel or bound was changed.

predictions/ retains the original bytes, with hashes in prediction-manifest.json;
the available original SHA-256 manifests were checked. score-frozen.py verifies
raw answers against the blind Git commit before joining IDs and comparing exact
bits/errors. Worksheet error spellings such as #NUM! are normalized to the
standard witness encoding error:Num. scores.json and score-rows.tsv retain every
column and every row. Reproduce with python probes/2026-10-31-calcvba-run4/score-frozen.py.
