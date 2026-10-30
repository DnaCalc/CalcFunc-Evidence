# W109 PERMUT Identification + COMBIN Findings — 2026-07-11

## PERMUT — identified and signed off

`PERMUT(n,k)` is the **ascending legacy x87 spill-loop product**:
`acc = RN53(RN64(acc · f))` for `f = n-k+1 ..= n`. Unique surviving candidate
out of 6 stagings (strict/spill/extended × forward/reverse) over 402 live
witnesses; production kernel (`permut_fn::permut_kernel`) verified
**702/702 bit-exact** across discovery + fresh held-out sweeps (build 20131).
The former factorial-ratio `n!/(n-k)!` staging was 1 ULP off on the catalog
witness `PERMUT(61,20)` and overflowed spuriously for `n > 170`.
In-crate pin: `permut_matches_live_excel_pinned_witnesses`.

## COMBIN — historical wall superseded by exact graph (2026-08-09)

The July dedicated-lgamma hypothesis is retracted. The exact current-reference
graph landed in `c879f3f`. After Excel-style truncation and
`k = min(k, n-k)`, `k=0` returns `1`; otherwise the graph walks `i=2..k` in
ascending order, stores `(n-k+i-1)/i` through `RN53(RN64(div))`, stores each
accumulator product through `RN53(RN64(mul))`, and finally multiplies by `n`
through the same stored-x87 publication operation. The characteristic `k=3`
schedule is `((n-2)/2) * ((n-1)/3) * n`.

The compiled production kernel is exact on `505/505` legacy-build rows,
`20,713/20,713` current-build discovery rows, and a candidate-frozen,
prior-disjoint held-out at `1,024/1,024`: `22,242/22,242` combined. Focused
Rust, the full core suite, focused Lean, and the full Lean build are green.

A later paired COMBINA boundary campaign qualified the previously unprobed
COMBIN admission seam without changing that body: DAZ precedes the raw
negative guard, truncated `n` is admitted only through `2_147_483_646`, and a
nonfinite cyclic accumulator returns `#NUM!` immediately. The original body
corpora remain exact; 2,195 new admission/control rows are also exact, so
combined COMBIN production replay is `24,437/24,437`. A genuinely fresh
76-row admission gate passed `76/76` without refinement. The shared admission
correction and COMBINA route landed in `3f31f44`.

This signs off only the current-reference `COMBIN` sublane with
`scope_completeness: scope_complete`, `target_completeness: target_complete`,
`integration_completeness: integrated`, and `open_lanes: []`. The other
independent members keep the mixed G4-04 row and aggregate `BUG-FUNC-027`
stream open. Scoped child bead `oxf-jwh5.9` is closed; the W109 parent remains
open. See
`W109_COMBIN_IDENTIFICATION_20260809.md` for controls, hashes, provenance, and
the scoped OPERATIONS Sections 12/14 audit.

## COMBINA — exact transformed-COMBIN graph (2026-08-09)

The July claim that no product graph could publish the observed inexact
integer, and that COMBINA therefore required GAMMALN, is retracted. COMBINA
applies DAZ and separately truncates both inputs; its zero/zero pool precedes
the asymmetric truncated-n/raw-DAZ-k negative guard; it then delegates
`trunc(n)+trunc(k)-1, trunc(k)` to the corrected COMBIN admission and cyclic
stored-x87 body.

Current production is exact on `40,330/40,330` typed COMBINA rows. The central
candidate-frozen prior-disjoint gate is `2,048/2,048`, and the genuinely fresh
fractional-ceiling/DAZ gate is `144/144` without refinement. Together with the
paired COMBIN gate the fresh publication result is `220/220`; the route landed
in `3f31f44`. The
current-reference COMBINA sublane is `scope_complete`, `target_complete`, and
`integrated`, with `open_lanes: []`; scoped child `oxf-jwh5.11` is closed
signed off. G4-04 remains open only for ERF/ERFC.PRECISE. See
`W109_COMBINA_IDENTIFICATION_20260809.md` for hashes, retired-v1 discipline,
controls, boundary semantics, and the Sections 12/14 audit.

## ACOTH — historical wall superseded by exact graph (2026-08-09)

The July blocking/inheritance interpretation is retracted. ATANH's exact graph
landed independently in `a03a75f`, and ACOTH does not use the former
reciprocal-ln1p helper. Its separate W109 campaign identified the exact
current-reference graph: native binary64 ratio add/sub plus one stored-x87
division below `0x400d92b14ec204f3`, and a direct inverse odd-power series with
stored-x87 reciprocal/multiply/divide/add above it. A subnormal reciprocal
publishes +0 for both signs.

The frozen prior-disjoint held-out passed `66552/66552`; the actual production
kernel replay is `268769/268769`. G4-03 and BUG-FUNC-027 CLASS-C5 are signed
off while the aggregate bug stream and wider W109 remain open. See
`W109_ACOTH_IDENTIFICATION_20260809.md` for exact endpoints, artifact hashes,
provenance, and the scoped audit.

## CONVERT — deferred (historical harness gap; superseded 2026-08-09)

CONVERT takes text unit arguments; `CellRefBatch.psm1` currently plumbs
numeric cells only. Needs a small harness extension (string-literal unit args
inside the formula text are bit-exact-safe) before the factor-bits probes can
run. Not attempted this pass.

This deferral no longer describes current state. The hardened typed runner and
exact-bit Value2 readback controls enabled a full clean-room campaign; the
identified graph landed in `8ef5cac`, passed the frozen prior-disjoint
`10418/10418` publication gate, and replays compiled production
`34189/34189`. See `W109_CONVERT_IDENTIFICATION_20260809.md`.
