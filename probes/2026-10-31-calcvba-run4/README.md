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
