# W109 Trig Identification And Sign-Off (G4-01) — 2026-07-11

> **2026-08-09 G4-07 correction:** the 2026-07-11 corpus remains valid bounded
> evidence, but its universal raw-FSIN odd-quadrant COS inference was false.
> Fresh exact-phase discovery and a frozen oracle-blind held-out identify the
> corrected odd-quadrant publication graph below. The correction landed in
> `ed9f222`; worksheet COS now replays `2561/2561`, and the dependent BESSELJ
> graph replays `794/794`.

Row `G4-01` (SIN/COS/TAN/COT/SEC/CSC, 1–5664 ULP argument-dependent drift) is
closed. All six calculation graphs were identified by the W109 search and
landed as `excel_sin` / `excel_cos` / `excel_tan` in
`oxfunc_core::excel_numeric` (routed by the six worksheet kernels; the
`|x| >= 2^27 -> #NUM!` guard was already aligned and is unchanged).

## Identified calculation graphs (live Excel 16.0 build 20131, x86-64)

```
SIN(x) = (-1)^Q · FSIN(r),  (r, Q) = FPREM1(x, FLDPI)           [fFSIN]
COS(x) = 1.0 exactly           if |x| < 2^-26  (live bit-ladder; 2^-26 itself
                                takes the chain and publishes 1 - ulp)
       = {FCOS(r), -S*(r), -FCOS(r), S*(r)}[Q mod 4],
         (r, Q) = FPREM1(|x|, FLDPI/2),
         t = FPTAN(r), S*(r) = sign(t) * FSQRT(t*t / (1 + t*t)),
         with the S* chain continuous in x87 PC64/RN and no binary64 spills
TAN(x) = FPTAN(r)              on even Q
       = -(1 / FPTAN(r))       on odd Q, reciprocal in EXTENDED before the
         single binary64 store; (r, Q) = FPREM1(x, FLDPI/2)     [fFTAN]
COT(x) = RN53(RN64(1 / TAN(x)))     (double-rounded recip of published TAN)
CSC(x) = RN53(RN64(1 / SIN(x)))
SEC(x) = RN53(RN64(1 / COS-chain(x)))   (composes to 1.0 at tiny x because
         recip-dr of 1-ulp ties back to exactly 1.0 — no branch needed)
```

**The reduction constant is the 64-bit ROM `FLDPI` π** — not the hardware's
internal 66-bit reduction (raw `FSIN`/`FPTAN` are ruled out by the recon
witnesses) and not any correctly-rounded π (platform libm ruled out, up to
1.27e9 ULP apart on large arguments). This is the whole source of Excel's
large-argument trig "error": δπ = RN64(π) − π ≈ +5.0e-20 scales linearly with
the quotient. The δπ back-solve from the 5664-ULP witness predicted the
`FLDPI` constant before the candidate was run — both recon witnesses then
matched bit-for-bit on the first try.

Key identification details discovered along the way:
- `FPREM1` reports quotient-MAGNITUDE bits, so COS (even) must reduce `|x|`
  for the mod-4 dispatch to be valid — negative-`x` probes caught this.
- COS is NOT `sin(x + π/2)` through the fFSIN chain (`87trig`-plausible but
  138/200 wrong) and NOT π-parity (1-ULP misses at residues near ±π/2).
- The COS `1.0` shortcut threshold was pinned to bit resolution:
  `2^-26 - ulp -> 1.0`, `2^-26 -> FCOS` (adjacent-ulp live ladder).
- The former odd-quadrant raw-FSIN branch scored `1023/1027` on the 2026-08-09
  discovery battery. The tangent-square reconstruction above is the unique
  tested family member to score `1027/1027` and then `514/514` on a frozen,
  oracle-blind candidate-disagreement hold-out.

## Sign-off

- The original per-function live rounds remain valid: SIN/TAN/COT/CSC/SEC
  **1020/1020** and COS **1044/1044** (the same 1020 validation rows plus a
  separate 24-row threshold ladder), max ULP 0. The original deduplicated
  production replay remains **5425/5425** (`verify_trig_promotion`).
- Corrected COS evidence adds a 1027-row adjacent/random discovery battery and
  a 514-row frozen oracle-blind hold-out. Counting the original 1020 validation
  rows, the selected production graph is **2561/2561**; the 24 threshold rows
  remain separate retained guard evidence.
- The dependent production BESSELJ replay is **794/794** after both J0/J1
  cosine sites consume the corrected graph and J0 alone stages `cosine*P`
  through `excel_x87_mul`.
- In-crate pins: `trig_matches_live_excel_pinned_witnesses` (the former
  catalog witnesses — 5664/719/351/230/1-ULP rows — plus the threshold).
- Workspace green (1495 lib tests).

## Direct consumers and adjacent-risk result

- Worksheet `COS` is the primary publisher; `SEC` consumes its published value
  through the already identified x87-double-rounded reciprocal composition.
- `BESSELJ` consumes worksheet COS at both asymptotic J0/J1 cosine sites; its
  separately staged J0 product is recorded under BUG-FUNC-046/G4-06.
- GAMMA reflection consumes the SIN substrate, not COS. The focused SIN phase
  ladder remained `25/25`, so G4-07 did not reopen GAMMA.
- The `raw` x87 primitive layer is now compiled unconditionally (the
  `research-x87` feature only gates the public research re-export).

## Ruled out (ledger updated)

Platform libm trig; raw hardware FSIN/FCOS/FPTAN (66-bit internal reduction);
FPREM/FPREM1 against 2π (with residue extended or stored); π-parity for
COS/TAN; `sin(x+π/2)` COS; strict (single-rounded) reciprocals for
COT/CSC/SEC; cos/sin ratio forms for COT. The 2026-08-09 extension additionally
rules out the former raw-FSIN odd branch (`1023/1027`), 960 explicit
quotient/product/subtract reducers (best `767/1027`), residue-spilled FPREM1
(`265/1027`), double-double series (`1020/1027`), public AMD/SSE2/FMA
polynomial variants (best `1009/1027`), and the alternate FPTAN normalization
forms (best `1025/1027`). The durable rows are in
`DISCREPANCY_RULED_OUT_LEDGER.csv`.
