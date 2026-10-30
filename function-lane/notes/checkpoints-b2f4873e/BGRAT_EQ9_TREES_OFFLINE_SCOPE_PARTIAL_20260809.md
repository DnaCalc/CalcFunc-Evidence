# W109 G3-01 BGRAT Eq-9 tree/mask race — offline scope-partial result

Date: 2026-08-09

## Outcome

No exact survivor emerged.  With the currently identified worksheet LN/EXP
chain and the q/u construction frozen, the best enumerated Eq-9 body schedule
matches 65 of 943 selection rows (61/822 b25 and 4/121 b21-sharp).  The native
source body matches 55/943 (53/822 and 2/121).  The bounded winner therefore is
a useful staging clue, not a BGRAT identification or promotion candidate.

The only useful body change is coherent but small:

- form `j0 = q/r` as an x87 PC64 division, then spill to binary64;
- form every `dj = d*j` as an x87 PC64 multiplication, then spill to binary64;
- retain the running `sum += dj` in x87 PC64 across iterations;
- keep v, t2/t, the j recurrence, cn, the inner s term, d, and the final u*sum
  on the native binary64 source schedule.

This schedule is encoded as `j0=t0/m001`, `sum=t0/m001`, and `native` for all
other statement families.  It scores 65/943 exact, worst absolute miss 158
ULP, and sum absolute ULP 21,833.  Exact-by-tag is A=56/678, B=0/94,
C=5/50, b21-sharp=4/121.

## Corpus and provenance boundary

Selection used only:

- b25: all 822 rows from `answers-b25-bgrat.json`, joined by id to
  `agentM_b25_meta.json`; the loader asserts row count, x bits, and recomputed
  `y = 1-x` bits.
- b21-sharp: 118 rows selected from `answers-b21-beta.json` by
  `b <= 1`, `x > 0.5`, `a > 15`, plus three matching b15/BGRAT rows from
  `agentF_bgrat_rows.json`; the loader asserts the combined count is 121.
- `answers-b9heldout.json` and every other held-out corpus were neither loaded
  nor used for ranking.

The four selected input artifacts do not embed Excel application
version/channel/build or workbook Compatibility Version metadata.  Their
expected bits are therefore banked black-box observations with incomplete
capture provenance.  This lane cannot promote a survivor even if one were
found until that provenance is attached or the candidate is replayed on a
frozen, versioned oracle capture.

No Excel process, COM interface, Microsoft binary, network resource, or
non-public implementation source was used.  The body is reconstructed from
the public CDFLIB `bgrat.f` source and public floating-point arithmetic.  The
only oracle evidence is the pre-existing answer banks.

## Frozen primitive caveat

`agentM_b25e.py` and `agentM_b25f.py` were starting references, not the final
primitive implementation.  This racer calls the repository's current
`research::excel_ln`, `research::excel_exp`, and `research::excel_exp_rz`
implementations.  Consequently, the frozen-primitives/native-body baseline is
53/822 + 2/121, not the older mpmath-emulated agentM score of 80/822 + 5/121.

The distinction is observable at the first b25 row.  The older Python
emulation produced `e2 = 0x3fdf1ba7e9ba8ac4`; the current exact worksheet
primitive produces `e2 = 0x3fdf1ba7e9ba8ac3`, which propagates to
`r = 0x3f99a7d0557c9ba3` and `u = 0x3f99a7ded1f91332`.  The source and primitive
dependency hashes below freeze the exact realization scored here.

## Enumerated graph family

A set mask bit means “spill this x87 PC64 result to binary64”; an unset bit
means retain the PC64 register value.  Each family also contains the native
source graph.

| Statement family | Trees/masks plus native | Configurations |
|---|---:|---:|
| `v` | 4 association trees with 2–3 spill sites | 21 |
| `t2` and `t *= t2` | 4 trees, three spill sites | 33 |
| initial `j = q/r` | one x87 division/spill site | 3 |
| j recurrence numerator | 12 trees, eight spill sites | 3,073 |
| `cn` division | 4 trees, three spill sites | 33 |
| inner s term/coefficient | 3 trees, four spill sites | 49 |
| `d` | 3 trees with 3–4 spill sites | 41 |
| `dj` and running sum | one tree, two spill sites | 5 |
| final `u*sum` | native or x87 PC64 | 2 |
| **Total isolated statement configurations** |  | **3,260** |

The combined search then ran two sum-seeded coordinate passes (6,510
full-corpus evaluations) and a width-64 beam using native plus the top four
choices from every association tree.  Per beam stage it evaluated 17, 289,
192, 3,136, 1,088, 832, 832, 320, and 128 unique full configurations,
followed by 64 final rescoring evaluations.  Including baseline and the final
coordinate score, the run performed 16,670 full-corpus configuration scoring
passes.  This is bounded enumeration/beam evidence; it is not an exhaustive
Cartesian product of all 3,260 statement choices.

## Ranked evidence

| Frozen-q/u body candidate | Exact | b25 | b21-sharp | Worst abs ULP | Sum abs ULP |
|---|---:|---:|---:|---:|---:|
| Native source | 55/943 | 53 | 2 | 158 | 21,892 |
| Best isolated `j0` graph | 55/943 | 53 | 2 | 158 | 21,891 |
| Best isolated `sum/dj` graph (`t0/m001`) | 65/943 | 61 | 4 | 158 | 21,835 |
| Coordinate/beam winner (`j0` + `sum/dj`) | 65/943 | 61 | 4 | 158 | 21,833 |

The best isolated v, t2, recurrence, cn, s, d, and final families all tie the
native 55 exact-row score and do not reduce the 158-ULP worst miss.

The signed residual histogram for the winner, clipped at ±16 ULP (the endpoint
bins are tails), is:

```text
{-16:208, -15:18, -14:20, -13:37, -12:43, -11:39, -10:28,
 -9:40, -8:32, -7:16, -6:14, -5:23, -4:34, -3:32, -2:24,
 -1:30, 0:65, 1:31, 2:16, 3:20, 4:13, 5:5, 6:2, 7:2,
 8:3, 9:1, 10:3, 11:2, 12:1, 14:1, 16:140}
```

Largest misses include:

```text
b21-a16-b0.45-k4  +158  got 0x3fc1515ffa68b615  want 0x3fc1515ffa68b577
b21-a31-b0.45-k5  +153  got 0x3fc24583695133b4  want 0x3fc245836951331b
b25C-a24-b0.45-k5 +149  got 0x3fc8ea4a7f0a42fb  want 0x3fc8ea4a7f0a4266
```

For the b25 tag-A shared-z intersection gate, 40 groups (671 rows) contain at
least two rows.  Among the final 64 beam candidates, only 2/40 groups have any
single candidate exact on every member, covering 4/671 rows; 38/40 groups have
no common candidate.  Each isolated statement family reaches only 1/40 groups
and 2/671 rows.  This strongly rejects the enumerated frozen-q/u body family as
the explanation for the Eq-9 wall.

## Reproduction and gates

From `C:\Work\DnaCalc\OxFunc`:

```powershell
rustfmt --edition 2024 --check smart-fuzzer/tools/calc_graph_racer/src/bin/race_bgrat_eq9_trees.rs
$env:CARGO_TARGET_DIR='C:\Work\DnaCalc\OxFunc\target-bgrat-eq9'
cargo build --offline --release --bin race_bgrat_eq9_trees --manifest-path smart-fuzzer/tools/calc_graph_racer/Cargo.toml
.\target-bgrat-eq9\release\race_bgrat_eq9_trees.exe smart-fuzzer\work\w109\G3-01-dist
cargo test --offline --release --bin race_bgrat_eq9_trees --manifest-path smart-fuzzer/tools/calc_graph_racer/Cargo.toml
```

Observed gates:

- loader assertions: pass (822 + 121; x/y bit joins checked);
- frozen current-primitive baseline assertion: pass (53 b25, 2 b21-sharp);
- offline release build: pass;
- `rustfmt --check`: pass;
- binary run: pass, deterministic headline scores over repeated runs;
- bin test harness: pass (zero unit tests; correctness gates are runtime
  assertions and exact corpus scores);
- held-out isolation: pass by loader construction; no held-out path exists in
  the binary;
- exact survivor: fail (best 65/943);
- shared-z intersection: fail (38/40 groups have no common final-beam
  candidate).

## Hash manifest (SHA-256 at the scored run)

```text
cfe2540541b0ef0b4dc7dbf672609932533705438101e4c9ac4198650f09f65f  smart-fuzzer/tools/calc_graph_racer/src/bin/race_bgrat_eq9_trees.rs
fd6e9919c8dedeeadd32817ec5dda88313f773c5468286f733f79e10f879bfdb  target-bgrat-eq9/release/race_bgrat_eq9_trees.exe
a71ffae003d4f4b9fd90c1678920a6d132c0f1566c95fd3c720a482b36bd0a02  smart-fuzzer/tools/calc_graph_racer/Cargo.toml
812920dbba3c03f5d02c2dfcb504bd306fd51289400a4432c20ed6dc39dc6094  smart-fuzzer/tools/calc_graph_racer/Cargo.lock
db43632b1c68febff0538bb5c058033f55360533e36f813bc762bbfc846689ab  crates/oxfunc_core/src/excel_numeric/research.rs
d76c466a126c087fb10135344be97a677e7ba0beeb10685af7f167aaf9df1e8c  crates/oxfunc_core/src/excel_numeric/mod.rs
29ff13ef5896ea23cf893dfdc263a6f3458bb70a7ca74ca59d2e54a2dec009b2  crates/oxfunc_core/src/excel_numeric/x87.rs
1cd5b94597c714cd215992cfa56fb67893a86f72f3875d7f46a120359cbecc27  smart-fuzzer/work/w109/G3-01-dist/answers-b25-bgrat.json
f09701bf7913a8216fccc69368866988fa997c438c61ea7c6a69d1e5d807727b  smart-fuzzer/work/w109/G3-01-dist/agentM_b25_meta.json
0aea562acb2026ff625b04d461935e635acb286b978f23c60d5dca07c2359f4a  smart-fuzzer/work/w109/G3-01-dist/answers-b21-beta.json
ac245201a581afc721b4711d9dff6c28a4da9e75f4187ff4c7675628cc036b90  smart-fuzzer/work/w109/G3-01-dist/agentF_bgrat_rows.json
f2e078380d5816a762cd5b714548c73ef05e32663521812d1bfc34191b34b34d  smart-fuzzer/work/w109/G3-01-dist/agentM_b25e.py
22c98ec65966951d31103bd939d0a66fbe4bcb9655ed96bc299edfa60ebc3226  smart-fuzzer/work/w109/G3-01-dist/agentM_b25f.py
9c5b9193ae1531d5dc78dd1eb6703b9bc07a7a3b26657d831c05930890ae347a  smart-fuzzer/work/w109/G3-01-dist/lane1_pdf_round6.py
e691caa74dc141f7d97f0a0e2243d1e5318ae8150ca660dcb462b7d2955d2c73  smart-fuzzer/work/w109/G3-01-dist/cdflib/bgrat.f
28251801cd92eda517a71ae12091b37d7bee5ba29ca788cbef41f15d1fa0e66a  smart-fuzzer/work/w109/G3-01-dist/diagnose_bgrat_eq9_frozen.py
```

Repository HEAD at the run was
`3c4a3b4dcc2004936cda488156879f1e7d3fdf59`.  The worktree contained unrelated
pre-existing/shared changes; the hashes, rather than HEAD alone, are the replay
identity for this lane.  The lane-only `target-bgrat-eq9` build directory was
removed after its hash audit; the binary hash records the scored build, while
the tracked report and Rust source are the durable replay artifacts.

## Status and next gate

- `execution_state: in_progress`
- `scope_completeness: scope_partial`
- `target_completeness: target_partial`
- `integration_completeness: partial`
- `open_lanes`:
  - q construction and q/r interface staging with the current LN/EXP chain;
  - u construction staging, including ALGDiv, `b*LN(nu)`, subtraction, EXP,
    and final product order;
  - joint q/u/body search after separately discriminating those primitive
    axes;
  - any source graphs not represented by the enumerated public Eq-9 trees;
  - versioned fresh/held-out replay if a coherent survivor later emerges;
  - production integration and documentation, neither authorized here.

Recommended next gate: keep the body winner only as a diagnostic seed, then
split q and u using implied-bit/shared-z constraints before any larger joint
beam.  There is no frozen capture request from this lane because no coherent
discovery survivor emerged.
