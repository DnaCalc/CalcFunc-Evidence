# W109 YIELDMAT Identification And Sign-Off — 2026-07-11

Row `G6-09` (YIELDMAT, 1-2 ULP) is closed. Identified by the W109
calculation-graph search (128-candidate space over bases 2/3 where day counts
are exactly replicable, then validated through the production kernel's full
basis logic on the basis-0/1 catalog witnesses) and landed in
`oxfunc_core::functions::bond_core_family::yieldmat_kernel`.

## Identified calculation graph (live Excel 16.0 build 20131, x86-64)

```
b     = days-in-year, dim = days(issue,maturity), a = days(issue,settlement)
dsm   = RN53(RN64(dim - a))
dbr   = RN53(RN64( RN53(RN64(dim/b)) · rate ))
accr  = RN53(RN64( RN53(RN64(a/b)) · rate ))
p     = RN53(RN64(price/100))
term2 = RN53(RN64(p + accr))
term1 = RN53(RN64( RN53(RN64(1 + dbr)) - term2 ))      <- term2 REUSED
yield = RN53(RN64( RN53(RN64(term1/term2)) · RN53(RN64(b/dsm)) ))
```

Legacy x87 spill-loop arithmetic (third confirmation after XNPV and NPER) with
the **published formula's association**: `term1 = (1 + DIM/B·rate) - term2`,
reusing `term2` — NOT the F#/ExcelFinancialFunctions left chain
`dim/b*rate + 1 - price/100 - a/b*rate` that OxFunc previously ported (1-2 ULP
off, ruled out).

## Search evidence

- Round 1 (150 live distinguishing probes from a 700-probe basis-2/3 pool):
  killed the entire first 72-candidate space — the miss pattern pointed at a
  missing term1 association; adding the docs-form (term2-reuse) variant and a
  year-fraction final division gave a 128-candidate space with exactly 2
  offline survivors (strict vs spill), both docs-form.
- Round 2 (35 window probes found by ranking a 60,200-probe full-entropy pool
  offline): killed strict; unique survivor `ym-spill-d100-dfrac-t1docs-ratio`.
- Validation: 1,250-probe live sweep (discovery + held-out, fresh seed),
  **1250/1250 bit-exact, max ULP 0**.
- Promotion: production kernel reproduces both former catalog witnesses
  (basis 1: `0x3faf3b645a1cabfe`, basis 0: `0x3faf37e9d4b23782`) — the
  identified staging transfers across the day-count bases as expected.

## Sign-off

- In-crate pins: `yieldmat_matches_live_excel_pinned_witnesses` (both catalog
  rows + the spill-loop window discriminator).
- `cargo test -p oxfunc_core --lib`: 1493 green.
- Oracle answers cached under
  `smart-fuzzer/cache/oracle/build-20131/YIELDMAT.jsonl`.

## Ruled out (ledger updated)

F#-style left-chain term1 (former OxFunc path); term1 variants
`dbr+((1-p)-accr)` and `(dbr+(1-p))-accr`; `price*0.01`; `(x·rate)/b` day
fractions; final associations `((t1/t2)·b)/dsm`, `(t1·b)/(t2·dsm)`,
`(t1/t2)/(dsm/b)`; strict (single-rounded) arithmetic.
