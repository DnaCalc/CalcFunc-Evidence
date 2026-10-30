# W109 G3-06 F.TEST variance/tail discovery checkpoint — 2026-08-09

## Scope and provenance

This is a clean-room, discovery-only checkpoint. It uses only the named W109
discovery banks, public F-distribution mathematics, and reproducible Excel
observations captured through the public worksheet interface. No Excel or
Microsoft binary was inspected. The publication heldout was not opened or
scored in this lane. Aggregate results for the retired 24-row wrapper
discovery are quoted only from the serialized root-lane report.

The discovery worker edited no production code, shared catalog/map/ledger,
BUG-FUNC record, workset, bead, or publication-heldout state. Root-owned
integration in the same evidence package reconciles the retraction in the
canonical catalog, calculation map, ruled-out ledger, and governing W109
notes; it does not promote a production graph or a completion claim.

Reference environment for the two new captures: Excel 16.0 build 20228,
64-bit, Workbook Compatibility Version 2, `cell_value2_bulk`, `NoCache`
hits/misses 0/0, with serialized Excel process counts 0 before and after.

## Corrected 48-row discovery score

The July score used unconditional `2 * live_FDIST_RT`. That is wrong whenever
the captured right tail exceeds 0.5. Three previously reported no-hit rows
are exact on the complementary side.

Using the corrected external composition

```text
tail <= 0.5 ? 2*tail : 2*(1-tail)
```

gives:

- accepted-group histogram `{0: 15, 1: 32, 2: 1}`;
- 33/48 rows with at least one exact candidate group;
- 30 low-tail exact rows and 3 complementary-side exact rows;
- unconditional `2*RT` exact on 30/48 rows;
- both forward, orientation-selected stored ratios score 32/48:
  `ratio=Native` 32/48 and `ratio=X87` 32/48;
- the ratio formed from the two live public `VAR.S` results scores 28/48;
- there are no exact-`F=1` candidate rows in this 48-row bank, so the
  equal-ratio boundary is reported separately rather than pooled here.

The loader now checks all 48 F.TEST, 350 FDIST, and 96 VAR.S ordered IDs and
arguments, verifies that the metadata group count equals the captured FDIST
count, and rejects every metadata/captured ratio-or-df mismatch. Per-row df
orientation is explicit (`A_over_B`, `B_over_A`, or equal-df ambiguous).

## Direct public-CDF discriminator

The root lane captured `F.DIST(x,df1,df2,TRUE)` for the already frozen ratio/df
groups. Scoring `2 * min(live legacy FDIST right-tail, live direct CDF)` leaves
the original 48-row result unchanged:

- histogram `{0: 15, 1: 32, 2: 1}`;
- 33/48 rows with an exact group;
- forward Native/X87 stored ratios 32/48 each;
- the same 15 rows remain no-hit.

The retired 24-row exact-variance wrapper discovery improves only to 15/24
under direct-CDF composition. All four reported ratio-4 controls are exact,
while the remaining misses are concentrated in the equal-ratio/boundary
surface. This is discovery evidence, not publication evidence.

Therefore replacing `1-RT` with the separately published direct CDF does not
make external distribution composition universal.

## Correctly oriented inverse-neighborhood refinement

The 15 corrected no-hit rows all use the low-tail branch and were only 1–5
output ULP from the target in the original 350-group bank. The v3 refinement
binds numerator and denominator dfs to each row's forward orientation-selected
stored-ratio key. It does not reuse `candidate_groups[0]` as a row-level df
shortcut.

The seed is an independent public incomplete-beta inverse. On the 33 known
exact discovery rows, using each accepted group's own df orientation, its
worst distance from an accepted live ratio is 40 input ULP. Each no-hit row
therefore receives:

- every ratio bit in a contiguous ±128-ULP window around the inverse seed;
- guard offsets ±256, ±512, ±1024, and ±2048 ULP;
- 265 probes per row, 3,975 unique FDIST probes overall.

The frozen answer-aware step read only the named v2 discovery answers. Its
future v3 answer file was absent at freeze time.

## v3 result and diagnosis

The v3 capture finds an exact external-FDIST equivalence ratio on only 4/15
rows:

| Row | Exact preimages | Delta from forward/public stored ratio |
| --- | ---: | --- |
| 22 | 3 | +1, +3, +4 input ULP |
| 29 | 1 | +1 input ULP |
| 36 | 1 | -1 input ULP |
| 38 | 1 | +3 input ULP |

None of those exact nearby ratios is an original frozen candidate key. They
are external FDIST-equivalence witnesses; they are not automatically Excel's
private F.TEST variance statistic.

For the other 11 rows:

- all 257 contiguous local inputs were captured;
- each local window brackets the F.TEST target;
- no local input publishes the target bit pattern;
- consecutive ratio inputs cross while skipping the target;
- the nearest observed result is 1 or 2 output ULP away;
- no row remains unbracketed by the frozen window.

Live FDIST has small local numerical non-monotonicities on several windows, so
this report does not claim that no remote external preimage exists anywhere.
It establishes the relevant result: the correctly oriented near-statistic
neighborhood cannot publish those 11 F.TEST bit patterns. Those misses cannot
be assigned solely to variance/statistic construction.

The evidence separates the residuals as follows:

- 3 of the former 18 no-hit rows were a scorer-side complement error;
- 4 of the corrected 15 admit nearby external equivalence ratios displaced
  1–4 input ULP from the forward/public stored ratio;
- 11 of the corrected 15 exhibit a local external-FDIST output skip, pointing
  to a graph-distinct private F.TEST tail/publication route in addition to any
  remaining variance-schedule question.

## Current-BRATIO private-tail staging race

A follow-up offline race evaluates the repository's current TOMS-708 BRATIO
body directly instead of composing separately published worksheet FDIST. For
every frozen ratio/df group it enumerates 3,200 deterministic graphs spanning:

- ordinary versus stored-x87 multiplication of `df1 * ratio`;
- ordinary versus stored-x87 denominator and both complement divisions;
- direct CDF and direct right-tail BRATIO calls, each component of the returned
  accurate-complement pair, and explicit ordinary/stored-x87 complements; and
- multiply-by-two and add-to-self on the selected smaller tail;
- direct `2-2p` and `2-(p+p)` from the original larger tail, with independent
  ordinary/stored-x87 scale, add, and subtract sites; and
- complement-first publication of the original larger tail with independent
  ordinary/stored-x87 complement and final scale/add sites.

No graph is close to an exact survivor. The best fixed graph is only `9/48`
whether allowed to choose any frozen ratio group, restricted to the forward
native-ratio group, or restricted to the forward stored-x87-ratio group. Across
the entire 3,200-graph family and all frozen ratio groups, only `12/48` F.TEST
target bit patterns are reachable at all. Candidate outputs are retained even
when they fall outside `[0,1]`, so the direct complement forms are scored rather
than pruned before comparison.

| Two-sided publication family | Any frozen ratio | Forward native ratio | Forward stored-x87 ratio |
| --- | ---: | ---: | ---: |
| `2*small` | 9/48 | 9/48 | 9/48 |
| `small+small` | 9/48 | 9/48 | 9/48 |
| `2-2*large` | 6/48 | 6/48 | 6/48 |
| `2-(large+large)` | 6/48 | 6/48 | 6/48 |
| complement-first double/add | 6/48 | 6/48 | 6/48 |

This result does **not** identify or rule out Excel's private incomplete-beta
body. It bounds a narrower hypothesis: wrapping the current production BRATIO
realization in the enumerated quotient/complement/publication stagings cannot
explain F.TEST. The exact beta-tail/bgrat realization remains an upstream
substrate lane, in addition to the F.TEST-private wrapper and variance schedule.
No new oracle call is justified by this negative race.

## Explicit July-claim retraction

Retract the universal July decomposition claim that Excel F.TEST is reproduced
bit-for-bit by `2 * FDIST(orientation-selected stored variance ratio, dfs)` (or
by its simple `1-RT`/direct-CDF complement variants). The current-build evidence
supports only a partial observational relation. Excel F.TEST's private
tail/publication graph is distinct from separately published FDIST/F.DIST on
the residual surface.

## Defects and coverage gaps found

1. The July scorer omitted the high-tail complementary branch, misclassifying
   three rows. The corrected histogram is the one reported above.
2. An early offline inverse calibration used dfs from `candidate_groups[0]`
   instead of the accepted ratio group. Eight known-hit rows change orientation
   relative to group 0; this produced spurious large inverse errors (including
   the false row-7 ~2.89 result). The durable tool binds dfs to each key.
3. The original discovery scorer checked 48 F.TEST and 96 VAR.S rows but did
   not assert that the captured FDIST count equals both metadata `fdist_count`
   and the sum of referenced groups. The durable loader asserts all three and
   rejects orphan/missing groups.
4. The original 350-row generator did not include a direct-CDF companion. The
   new companion closes that discovery coverage gap but does not improve the
   48-row score.

## Reproducible artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `race_ftest_variance.rs` | 51,064 | `872C94F1E1AC7FB8C5902EE84D4B50A31C4937F00B703002A710461BB17B800F` |
| `race_ftest_private_tail.rs` | 14,259 | `144AD1A4EF9A2562E2A940408DC9E69FE95F243F768C464EB045E8809CFCC66D` |
| `refine_ftest_variance_fdist.rs` | 60,423 | `B0E3A2F700E985193EAB5D391F1064B085945F1E18CFEB5BCE37C28A319332CC` |
| `invert_ftest_variance_target.rs` | 5,786 | `4927DFBB9DBBAFA6FBBF638722D841427D37EFBAF0B16BC01C13AF9E6472B594` |
| `audit-ftest-variance-discovery-v2.json` | 84,814 | `3068FE549F4A02C7B255F2DFCD24F9F37D205ED9B0B59612E443C9F56E21DE43` |
| `batch-fdist-cdf-companion-discovery-v1.json` | 97,294 | `9945E0ACDFEF987CBB8DB7CE047030DEF29148357A32C27A66E4D9CE91BC64C5` |
| `meta-fdist-cdf-companion-discovery-v1.json` | 68,908 | `B7480334CFEDF81885DF1E3C887B31A93C774AEEBB84B0C3E157C3263E49BDE9` |
| `answers-fdist-cdf-companion-discovery-v1.json` | 85,423 | `E9DE15EAFFADFD547D88B1FC95B4DF5A073E62821271F30D31D8B768EB7AEAB3` |
| `batch-fdist-variance-refinement-discovery-v3.json` | 997,838 | `6646764CF114514D98234CA35EB657C19A93F60E8C82D08005FDE78B5B67023A` |
| `meta-fdist-variance-refinement-discovery-v3.json` | 508,414 | `D7A4EC1A98E450ECDC5B6ADA2A087AAC0B6CE4A6E5FEEAC9049034F5B84806F8` |
| `answers-fdist-variance-refinement-discovery-v3.json` | 867,339 | `87845C9B174F62C39962C3858F499CD2E64CE9C61D3B1F58DF0926131A2F84C2` |
| `score-fdist-variance-refinement-discovery-v3.json` | 21,226 | `ADBBFCE0CFCB8B90A2BFAE5483D6E252A4B5DF4F4A5787C56B103AF5F4BB4E3D` |

The v3 metadata embeds the seven source path/byte/SHA entries, the exact batch
SHA, unique-count/orientation assertions, the absent-at-freeze answer path, and
the build/x64/CV2/Value2/NoCache pre/post-zero capture contract.

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial`
- `target_completeness`: `target_partial`
- `integration_completeness`: `partial`
- `open_lanes`:
  - identify the private F.TEST tail/publication graph on the 11 local-skip rows;
  - identify the upstream beta-tail/bgrat body rather than treating the
    current production BRATIO realization as exact;
  - separate the remaining private variance schedule from quotient and tail staging, preferably with a future answer-blind exact-control `B=[-1,0,1]` discovery if root reopens oracle work;
  - freeze an independent publication heldout only after one coherent private-graph survivor exists;
  - production, workset, BUG-FUNC, bead, and formal integration remain
    unattempted; the root-owned canonical evidence/retraction surfaces are
    reconciled without narrowing the open function scope.
