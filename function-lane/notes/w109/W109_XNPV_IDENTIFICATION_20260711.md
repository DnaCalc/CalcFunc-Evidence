# W109 XNPV Identification And Sign-Off — 2026-07-11

Row `G6-11` (XNPV, 16 ULP catalog witness) is closed. The calculation graph was
identified by the W109 active model-discovery loop (calculation-graph racer +
persistent Excel oracle + distinguishing-input scheduler) and landed in
`oxfunc_core::functions::cashflow_rate_family::xnpv_kernel`.

## Identified calculation graph (live Excel 16.0 build 20131, x86-64)

```
guard:  rate <= 0 (including -0.0)      -> #NUM!   (+1e-300 evaluates)
base  = RN53(RN64(1 + rate))                        x87 double-rounded add
per cashflow i (forward order):
  years = (date_i - date_0) / 365                   strict binary64 divide †
  pow   = POWER(base, years)                        FULL worksheet POWER kernel
                                                    (integer years -> binexp
                                                    publication, fractional ->
                                                    x87 exp(RN53(RN64(y·ln x))))
  term  = RN53(RN64(value_i / pow))                 x87 double-rounded divide
  total = RN53(RN64(total + term))                  per-step-stored x87 add
                                                    (legacy memory-spill loop)
```

† The double-rounded form of the years division is observationally equivalent:
an exhaustive scan of every integer day delta `1..2,900,000` (the whole Excel
date domain) found **zero** inputs where `delta/365` hits a double-rounding
window. The strict form is implemented.

Interpretation: XNPV's function body is legacy x87-compiled code — every
arithmetic assignment runs at extended precision and spills to a binary64
memory slot, extending the W108 "Excel transcendentals are x87" finding to the
surrounding arithmetic of this function.

## Newly discovered and fixed in the same change

Live Excel publishes `#NUM!` for `rate = 0`, `rate = -0.0`, and every negative
rate (probed at `-1e-300`, `-1e-9`, `-0.5`, `-1`, `-1.5`); `+1e-300` evaluates.
OxFunc previously accepted `(-1, 0]`. The surface guard is now `rate <= 0`.
XIRR's internal solver substrate (`xnpv_kernel_raw`) is intentionally
unchanged — its iterates legitimately evaluate at negative rates, and its
staging is a separate G6 solver-lane identification.

## Search evidence

- Candidate space: 480 graphs (years staging x base add x POWER kernel flavor
  x term staging x accumulation order/model), all as serde-JSON data under
  `smart-fuzzer/work/w109/G6-11-xnpv/`.
- Round 0 (offline, recon bits): 2 witnesses killed all platform-`powf` and
  end-stored extended-accumulator variants.
- Round 1 (live, 120 distinguishing probes from an 800-probe pool): killed
  every remaining candidate — the misses exposed the missing integer-exponent
  POWER dispatch (killing witness had `years = 5.0` exactly) and forced the
  per-step-stored accumulation axis into the space.
- Round 2 (live, 72 constructed double-rounding-window probes): separated the
  base-add / term-divide / summation axes; 2 survivors remained, differing
  only on the domain-equivalent years axis.
- Validation (live): 1,854-probe sweep over discovery + held-out (fresh seed,
  never searched) + metamorphic pools (power-of-two value scaling, joint
  (value,date) permutations, same-date splits) + guard probes.

## Sign-off

- Production-kernel replay over every deduplicated answered oracle witness:
  **numeric 1530/1530 bit-exact, error rows 175/175 matching `#NUM!`**
  (`calc_graph_racer verify_xnpv_promotion`).
- In-crate pins: `xnpv_matches_live_excel_pinned_witnesses` (one pin per
  identified axis) and `xnpv_rejects_zero_and_negative_rates_on_surface`.
- Oracle answers cached under `smart-fuzzer/cache/oracle/build-20131/XNPV.jsonl`
  (env pinned: Excel 16.0 build 20131, AMD reference host).

## Ruled out (see DISCREPANCY_RULED_OUT_LEDGER.csv)

Platform `powf` per term; fractional-only POWER staging (no integer binexp
dispatch); `(d-d0)*(1/365)` reciprocal-multiply years; reverse accumulation;
end-stored extended accumulator; strict (single-rounded) `1+rate`; strict and
extended-continuous term divide; `value * POWER(base, -years)` reciprocal
staging; plain strict forward sum.

## Reproduction

```
cargo run --bin gen_xnpv_space -- smart-fuzzer/work/w109/G6-11-xnpv
cargo run --bin gen_xnpv_adversarial -- smart-fuzzer/work/w109/G6-11-xnpv
cargo run --bin calc_graph_racer -- race|distinguish|eliminate ...
smart-fuzzer/tools/Run-W109ProbeBatch.ps1 -Batch <batch> -Out <answers>
cargo run --release --bin verify_xnpv_promotion -- <answered witness sets>
```
(from `smart-fuzzer/tools/calc_graph_racer`)
