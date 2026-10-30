# W109 NPER Identification And Sign-Off — 2026-07-11

Row `G6-08` (NPER, 1 ULP on NPER-0000) is closed. Identified by the W109
calculation-graph search (40-candidate space, two live rounds, constructed
double-rounding-window probes) and landed in
`oxfunc_core::functions::financial_time_value_family::nper`.

## Identified calculation graph (live Excel 16.0 build 20131, x86-64)

```
rate == 0 (either sign, EXACT — no epsilon band):
    nper = RN53(RN64( -(RN53(RN64(fv+pv))) / pmt ))        (#DIV/0! on pmt=0)
else:
    tf    = RN53(RN64(1 + rate·type))
    tfp   = RN53(RN64(tf·pmt))
    num   = RN53(RN64(tfp - RN53(RN64(fv·rate))))
    den   = RN53(RN64(tfp + RN53(RN64(pv·rate))))
    ratio = RN53(RN64(num/den))                              (<=0 -> #NUM!)
    nper  = RN53(RN64( ln_x87(ratio) / ln_x87(RN53(RN64(1+rate))) ))
```

Same signature as XNPV: a **legacy x87 spill-loop body** — every assignment
double-rounded, both logarithms the x87 worksheet `ln` (`fldln2`+`fyl2x`),
the denominator taken on an already double-rounded `1+rate`.

## Live-probed lanes (all newly pinned)

- Tiny nonzero rates take the MAIN path — there is **no epsilon branch**
  (OxFunc previously used `|rate| < 1e-12`): Excel degrades numerically
  (1e-9/1e-12/1e-15 reproduce bit-exactly through the main path) and returns
  `#DIV/0!` once `1+rate` rounds to exactly 1 (~1e-18 and below).
- `NPER(0, 0, ..)` publishes `#DIV/0!` (OxFunc previously `#NUM!`).
- `pmt = 0` on the main path publishes `#NUM!`; `rate <= -1` publishes `#NUM!`.
- The zero-rate linear branch is itself double-rounded: all 24 constructed
  add/divide window probes contradict strict staging.

## Search evidence

- Round 0 (offline, 2 recon witnesses): killed 28/40 — both logs proven x87
  (`platform ln` reproduces OxFunc's old 1-ULP miss exactly), FYL2XP1/log1p
  denominators off by ~800 ULP-scale.
- Round 1 (58 live distinguishing probes from a 912 pool): killed strict
  arithmetic (spill-loop confirmed) and the platform denominator.
- Round 2 (40 constructed window probes): separated base staging and final
  divide; unique survivor `nper-spill-xln-xlndr-drdiv`.
- Validation: 1,734-probe live sweep (discovery + held-out + branch),
  1,729/1,729 main-path rows bit-exact, max ULP 0; the 5 remaining rows are
  the zero/tiny-rate branch probes that pinned the branch rule.

## Sign-off

- Production-kernel replay over every deduplicated answered witness:
  **numeric 1286/1286 bit-exact, error rows 7/7**
  (`calc_graph_racer verify_nper_promotion`).
- In-crate pins: `nper_matches_live_excel_pinned_witnesses` (one pin per
  axis + error lanes), replacing the W108 `nper_denom_log_choice` pins that
  froze the superseded portable-CR path.

## Ruled out (ledger updated)

Portable/platform ln (numerator or denominator); FYL2XP1 and portable log1p
denominators; strict (single-rounded) arithmetic anywhere in the body; strict
final divide; strict `1+rate` base; any epsilon small-rate branch; strict
linear zero-rate branch.
