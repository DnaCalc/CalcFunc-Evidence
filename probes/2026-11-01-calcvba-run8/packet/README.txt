Round 10: PMT observation audit (64 calls, zero new answers).
From the updated DnaCalc master on Windows:
 cargo xtask witness read --func PMT --inputs <packet>/requests-PMT.json
Do not pass --new-only. These are intentional rechecks and transport pairs.
Run once, retain the frozen predictions, readings file and entire worker directory.
Compare all 32 numeric rows with PMT-predictions-historical.jsonl by ID.
Then compare paired literals/logical timing/text-rate results with their numeric row.
Only unchanged read-back inputs support same-input build comparisons. Literal echo
cells expose the decimal parser, not effective callee internals. Changed inputs and
unread results remain failed audit obligations, never semantic contradictions.
The adapter retains input_audits even for changed/refused rows. Preserve its raw
request.json/result.json. Record actual build, CPU/bitness and settings; do not
silently attribute build/CPU/surface differences to any one cause. No old observation
is overwritten. Historical transport and Compatibility Version are unknown.
32 numeric calls: 24 certified gaps (16 build20131,8 build20228),8 exact passing
controls (4 per build). Plus16 literal pairs,8 logical-timing,8 text-rate pairs.
Only requests-PMT.json is submitted. Predictions and old answers are separate.
This audit cannot claim build20527 reproduction until Windows returns readings.
