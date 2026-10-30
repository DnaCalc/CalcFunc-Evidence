# W109: COMBIN exact graph identification

Status: `closed_signed_off` for the current-reference `COMBIN` sublane of the
mixed G4-04 row

Identification, frozen gate, implementation, and verification: `2026-08-09`

Implementation commit: `c879f3f`

This report preserves the original COMBIN-body publication gate. The later
COMBINA campaign independently closed `COMBINA` and qualified a shared COMBIN
admission seam; see `W109_COMBINA_IDENTIFICATION_20260809.md`. The enclosing
G4-04 row now remains open only for `ERF`/`ERF.PRECISE` and
`ERFC`/`ERFC.PRECISE`.

## 2026-08-09 shared-admission addendum

Shared-admission implementation commit: `3f31f44`

Paired COMBINA/COMBIN boundary discovery showed that the signed-off cyclic body
also has a previously unprobed admission layer: both inputs use DAZ, remaining
raw negative values are rejected before truncation, and truncated `n` is
admitted only through `2_147_483_646`. The next integer is `#NUM!`, even for
`k=0`. A nonfinite cyclic accumulator can return `#NUM!` immediately because
complement reduction makes every remaining factor greater than one.

The original `22,242/22,242` body corpora remain exact. New paired controls,
retired-v1 DAZ discovery, and a genuinely fresh 76-row admission publication
gate replay `2,195/2,195`; combined COMBIN replay is `24,437/24,437`. The fresh
gate is `76/76` without refinement, while no-DAZ and raw-value-ceiling controls
score `66/76` and `62/76`. Lean and `FDEF-071` now record the admission layer
without changing the identified cyclic body.

## Identified current-reference graph

After Excel-style truncation and `k = min(k, n-k)`:

```text
if k == 0:
    return 1

acc = 1
for i = 2 .. k, ascending:
    factor = RN53(RN64((n-k+i-1) / i))
    acc    = RN53(RN64(acc * factor))

return RN53(RN64(acc * n))
```

The loop therefore evaluates numerator factors `n-k+1 .. n-1` against
denominators `2 .. k`, stores every quotient and accumulator product from x87
PC64 to binary64, and multiplies `n` only after the loop through the same
stored-x87 publication operation. The characteristic `k=3` fingerprint is
`((n-2)/2) * ((n-1)/3) * n`.

The simplest representative uses direct x87 division for each factor. An
unspilled x87 reciprocal-multiply spelling is observationally equivalent on
all `22,242` answered rows and a separate `231,073`-pair answer-blind finite
pool. This remaining instruction-level ambiguity has no known output-semantic
consequence.

## Black-box evidence and provenance

| corpus | profile / role | exact score |
|---|---|---:|
| July legacy bank | build 20131 discovery | `505/505` |
| current dense bank | build 20228 discovery | `20,713/20,713` |
| frozen publication gate | build 20228 prior-disjoint held-out | `1,024/1,024` |
| combined | both profiles | `22,242/22,242` |

The current discovery bank contains `16,641` dense reduced-triangle rows,
`3,652` raw mirror rows, and `420` deduplicated legacy additions. All `503`
overlapping tuples are bit-identical between builds 20131 and 20228.

The frozen held-out was selected answer-blind from `231,073` finite candidate
pairs with zero overlap against all `20,713` current discovery tuples. It
contains `384` PC53/store discriminators, `256` graph/order discriminators,
`256` broad hashed rows, `64` small-k fingerprints, and `64` mirrors. The
candidate and predictions were frozen before Excel answers were captured.

The sign-off profile was Excel `16.0` build `20228`, 64-bit, workbook
Compatibility Version `2`, `Range.Value2` argument injection,
`cell_value2_bulk` result capture, and `-NoCache`. The serialized capture
started with zero Excel processes and completed bounded teardown with zero
Excel processes.

Held-out controls:

| declared model | exact | mean absolute ULP | worst ULP |
|---|---:|---:|---:|
| selected stored-x87 cyclic graph | `1,024/1,024` | `0` | `0` |
| native PC53 cyclic graph | `606/1,024` | `0.8203125` | `9` |
| continuous x87 cyclic graph | `165/1,024` | `2.852539` | `20` |
| forward factor ordering | `179/1,024` | `2.405273` | `15` |
| correctly rounded integer | `165/1,024` | `2.851563` | `20` |

### Artifact hashes

Base directory: `smart-fuzzer/work/w109/G4-04-combin/` (gitignored evidence).

| artifact | SHA-256 |
|---|---|
| `batch-r1-excel.json` | `53F6B6BE3927DFD21FBD050497646B1411627E8C1F5494BA5D31BCAC39E2A77B` |
| `answers-r1-excel.json` | `97C57CD5529D53A7D73E8E18670C01363DECAA7B237909FFBE62A5C3772F7FDE` |
| `batch-current-discovery-v1.json` | `A5005141CAF3128D2140A36E591EC986DA7EAAC9DCBBAA049E6EB2A9BCA06D02` |
| `answers-current-discovery-v1-excel.json` | `E6180F57DFD1A51DAD623A27D6424101BBC1BCF1B9F0520B2901CCA5C60CFEB9` |
| `batch-cyclic-heldout-v1.json` | `5351A70F5A44E6F53BF7B4D994BB60C8573F43EE31ED08EFB9F0DBC7DC2C52B8` |
| `batch-cyclic-heldout-v1.meta.json` | `04B0758CF509FB616BC022FDF1C6D256D1B96053CDE19318199F7C5AD48136FE` |
| `predictions-cyclic-heldout-v1.json` | `3DDAA2252DA504D0FF3A7E4E5AF381463570CC7481695CA606621C00E98EBCA9` |
| `answers-cyclic-heldout-v1-excel.json` | `AB3EA44DDE976E4EA163FC369C5F63C21721B13EB56EACE7965A1A757EAAC0E6` |

Tracked replay source:
`smart-fuzzer/tools/calc_graph_racer/src/bin/replay_combin_production.rs`
(`A891330C6C86248EB92B5489C4AF4648FDAF203F5818F73BA959BE6DE23B7174`).

## Production and formal alignment

The original body commit `c879f3f` changed only:

- `crates/oxfunc_core/src/functions/combin.rs`, which implements the cyclic
  stored-x87 graph and exact current/held-out pins;
- `formal/lean/OxFunc/Functions/Combin.lean`, which records complement
  reduction, cyclic order, store sites, and final-`n` placement without
  duplicating the x87 engine.

At that original gate `COMBINA` and every other G4-04 function were untouched.
The later scoped package changes COMBINA and the shared admission layer under
the separately frozen evidence in `W109_COMBINA_IDENTIFICATION_20260809.md`.

The sign-off state package also tracks `replay_combin_production.rs`, which
requires the COMBIN function tag, unique nonempty IDs, strict argument/result
bit strings, numeric finite outcomes, and the captured finite COMBIN domain;
it reproduces all three corpora at `22,242/22,242` from a clean checkout plus
the hashed evidence files.

Verification:

- focused Rust: `13` passed;
- full `oxfunc_core`: `1,527` passed, `0` failed, `4` ignored, including all
  integration and doc-test targets;
- production replay: `22,242/22,242` exact;
- focused Lean: `6/6` jobs;
- full Lean: `492/492` jobs;
- exact-file Rust formatting and exact-path `git diff --check`: passed.

No FEC/F3E admission, coercion, type, shape, host, or evaluator-facing clause
changed. No OxFml handoff is required, and the XLL verification seam is not
material to this scalar numeric graph.

## Scoped closure audit

Status axes for `COMBIN` itself:

- `scope_completeness: scope_complete`
- `target_completeness: target_complete`
- `integration_completeness: integrated`
- `open_lanes: []`

Status axes for the enclosing G4-04 row and W109 campaign:

- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `open_lanes`: `ERF`/`ERF.PRECISE`, `ERFC`/`ERFC.PRECISE`, remaining catalog
  rows, broad post-catalog discovery, and declared version/CV axes.

### OPERATIONS Section 12 — Pre-Closure Verification Checklist

1. Contract/admission surface: pass; `FDEF-071` binds the exact body and the
   later DAZ/ceiling admission correction without changing coercion semantics.
2. Formal alignment: pass; the Lean route records the load-bearing body and
   corrected DAZ/ceiling admission schedule.
3. Rust implementation/tests: pass; focused and full suites are green.
4. Deterministic replay: pass; the retained body plus admission controls are
   `24,437/24,437` exact, including the fresh `76/76` admission gate.
5. Evidence/provenance: pass; exact bits, capture profile, process counts,
   selection discipline, retired-v1 discipline, fresh controls, and artifact
   hashes are recorded.
6. Version axes: pass for the declared current build-20228/x64/CV2 target;
   build-20131 overlap is separately recorded without a universal claim.
7. Public algebra versus empirical behavior: pass; Excel's intentionally
   inexact stored graph is retained where a rounded integer would differ.
8. XLL seam limitation: not material.
9. Cross-repo impact: pass; no handoff is required.
10. Known `COMBIN` semantic gaps: none on the declared target.
11. Completion-language audit: pass; claims are scoped to `COMBIN`.
12. State synchronization: pass; this report,
    the mixed-row supersession, `FDEF-071`, the `BUG-FUNC-027` stream/register,
    and the root-owned catalog/map/workset/worklist surfaces are synchronized
    while the enclosing G4-04 row remains open only for ERF/ERFC.PRECISE.
13. Bead state: pass; scoped child `oxf-jwh5.9` contains the evidence and is
    closed while the W109 parent remains open.

### OPERATIONS Section 14 — Completion Claim Self-Audit

1. Scope re-read: pass; this report claims only COMBIN; COMBINA is signed off
   separately and no mixed-row closure is claimed.
2. Gate criteria re-read: pass; discovery, frozen held-out, implementation,
   formal route, regression pins, and full verification are present.
3. Silent scope reduction: pass; truncation, complement reduction, small-k,
   mirrors, factor order, store precision, magnitude, and overflow are covered.
4. Looks-done-but-is-not audit: pass; the result is not tolerance-based,
   compile-only, cache-only, or refined from the publication gate.
5. Active-surface and bead audit: pass; all
   synchronized active surfaces retain the mixed-row qualification and scoped
   child `oxf-jwh5.9` is closed without closing the W109 parent.
6. Result: pass for the declared `COMBIN` sublane only.
