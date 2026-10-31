# Blind Excel readings for dna-firehorse round 7

38 POISSON.DIST requests, copied unchanged from codex-runs/fresh-questions-r7/requests.json.
Only requests.json was used as input. No prediction file was opened, ingested or scored.
The five deliberate control pairs and all Boolean/Double false variants were retained;
no --new-only filter was used. This is a selected research sample, not a parity rate.

DnaCalc-cfml was pulled with --no-rebase before use: c62ffca1e48b61989e7b481f9243a44fb6576b50.
launcher.rs calls its existing calc-oracle-excel::read_witnesses directly and uses
calc-verdict's argument decoder; it calculates no predictions. The existing witness
worker, Value2 readback and run_isolated process supervisor are unchanged. Source,
manifest, lockfile, worker scripts, raw requests/results and isolation record are retained.
Replay: build launcher.rs as src/main.rs with launcher-Cargo.toml as Cargo.toml in an
external temporary folder; pass a fresh folder containing requests.json to the executable.
Adjust dependency paths to the recorded DnaCalc revision. Do not overwrite this run.

All 38 answers passed exact typed input readback. The first two arguments are Double;
the third is Boolean false for 19 rows and Double zero for 19 rows. Test-Kept in the
worker verifies both managed type and exact bits/value. argument-types.json records
every row's checked types and result kind. All 38 results are binary64 numbers.
The standard reading is readings/excel-20527/POISSON.DIST-calcvba7.json.

Excel 16.0 build 20527, file 16.0.20527.20088, x64; Windows NT 10.0.26200.0;
AMD Ryzen 7 4800H with Radeon Graphics. AutomationSecurity was 1 before and after.
No Trust Center, macro-security or registry setting changed. Owned Excel PID 32320
exited normally. Pre-existing PID 3144 was left running. No DnaCalc source was edited.

Checks: python probes/2026-10-31-calcvba-run7/verify-blind.py;
python archive-evidence.py verify --all; python archive-evidence.py --set w109 verify --all.
