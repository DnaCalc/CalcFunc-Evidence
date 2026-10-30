# W109 EFFECT / RRI / NOMINAL Calculation-Graph Identification — 2026-08-09

This record captures the W109 black-box identification evidence for
`EFFECT`, `RRI`, and `NOMINAL` on the current reference host. It is an
identification-and-repair record for three now-landed bug slices, not a wider
financial-family, function-phase, W109-workset, or global campaign sign-off.

## Status

- `execution_state: complete` for BUG-FUNC-043/044/045
- `scope_completeness: scope_partial` relative to the wider W109
  financial/campaign scope; the three declared bug slices are closed and signed
  off
- `target_completeness: target_complete` for the exercised current-reference
  Excel build-20228/CV2 identification target
- `integration_completeness: integrated` for these three repairs at `876635e`
- `open_lanes:`
  - the wider W109 financial and discrepancy-catalog lanes, including the
    PMT/IPMT/PPMT/CUM family and every other still-open row;
  - the ordinary orthogonal alternate-version, alternate-channel, and locale
    sweeps, which are outside this identification packet.

No global, financial-family, W109-workset, or function-phase closure claim is
made here. The characterized graphs, including EFFECT's exact large-period
dispatch and RRI's DAZ/identity edge routes, passed their focused, full-suite,
formal-alignment, and landed-reference gates. Their implementation, exact pins,
contract/formal alignment, and evidence record landed in `876635e`; the open
lanes above do not reopen these three current-reference bug slices.

## Reference host and clean-room provenance

All new live observations in this record were obtained through the public
Excel worksheet interface with:

```
Excel application:      16.0 build 20228, 64-bit
Workbook compatibility: CompatibilityVersion 2
Operating system:       Windows NT 10
Runner:                 Run-W109BulkBatch.ps1, w109-bulk-batch-v2
Cache policy:           -NoCache
```

Seven held-out/follow-up sets were serially recaptured after discovery and embed
this provenance directly. Their batch IDs and ordered arguments were checked
against the requested batches, their results were replayed against the
selected production graphs, and their fresh SHA-256 values appear in the
witness ledger below. The eight-row `NOMINAL` wrapper-staging witness set also
embeds this provenance (`captured_utc = 2026-08-09T01:56:35.6146290Z`,
PowerShell 7.6.3). The EFFECT and RRI wrapper-staging files retain contextual
same-session provenance rather than embedded metadata, so that distinction is
preserved in the ledger.

The work is strictly behavioral. No Microsoft binary was disassembled,
decompiled, dumped, or otherwise inspected.

## Notation

For a basic operation `op`, define:

```
DR(op) = RN53(RN64(op))
```

That is the legacy x87 spill signature: evaluate under the 64-bit x87
significand and then publish to binary64. `LN_x87` and `EXP_x87` denote the
identified Excel x87 logarithm and exponential substrates, each published to
binary64. Hex values below are raw IEEE-754 binary64 bits.

## EFFECT — identified valid-numeric graph and large-period dispatch

For valid positive inputs:

```
n        = trunc(npery)
periodic = DR(nominal_rate / n)
base     = DR(1 + periodic)

if n < 4_294_967_295:                 # u32::MAX
    acc      = 1
    factor   = base
    e        = uint32(n)
    while e != 0:
        if (e & 1) != 0:
            acc = DR(acc * factor)
        e = e >> 1
        if e != 0:
            factor = DR(factor * factor)
    powered = acc
else:
    ln_base = LN_x87(base)             # publish binary64
    product = DR(n * ln_base)
    powered = EXP_x87(product)         # publish binary64

result = DR(powered - 1)
```

Below `u32::MAX`, the integer-power graph is right-to-left/LSB-first binary
exponentiation. The
essential distinction from the worksheet `POWER` integer helper is that every
accumulator multiplication and every factor squaring publishes through the
x87 double-rounding boundary. The wrapper division and `1 + periodic` add are
also x87 spill operations. At the exact truncated count `u32::MAX`, Excel
switches to the stored-base raw x87 logarithm/product/exponential chain; it does
not return an error and does not wait for the `u64` range boundary.

### EFFECT candidate scores

| Candidate | Banked grid | Fresh held-out | Combined |
|---|---:|---:|---:|
| x87-DR LSB-first integer power | 315/315 | 870/870 | **1185/1185** |
| ordinary-f64 LSB-first integer power | 305/315 | 770/870 | 1075/1185 |
| x87-DR MSB-first integer power | 253/315 | 355/870 | 608/1185 |
| x87-DR repeated multiplication | 204/315 | 260/870 | 464/1185 |
| raw logarithm/exponential power chain | 225/315 | 285/870 | 510/1185 |
| native `powf` | 244/315 | 286/870 | 530/1185 |

The broad grids did not distinguish all base-wrapper stagings: native versus
x87 division and native versus x87 addition collapsed at 1185/1185. Targeted
double-rounding-window probes then selected the x87 add 4/4. Two algebraic
rewrites were independently rejected on the held-out set:
`(n + nominal_rate) / n` scored 826/870, and
`nominal_rate * (1/n)` scored 869/870.

A fresh 160-row extreme-domain battery then located the dispatch exactly and
covered counts from `2^30` through `f64::MAX`: the final hybrid graph scored
`160/160` exact and `160/160` by kind. The former `u64`-guarded production
representative scored `144/160` exact; a raw-chain-only model scored `146/160`.
Excel returned 146 numeric values and 14 `#NUM!` overflows.

### EFFECT discriminator pins

Core integer-power pins:

| `nominal_rate` bits | `npery` bits / value | Excel result bits |
|---|---|---|
| `0x3ef4000000000000` | `0x4014000000000000` / 5 | `0x3ef4000a00020000` |
| `0x3fe9000000000000` | `0x4069000000000000` / 200 | `0x3ff2e4e18daed698` |

Targeted base-add pins, all selecting `DR(1 + periodic)` over an ordinary
binary64 add:

| `nominal_rate` bits | `npery` bits / value | Excel/x87 result | ordinary-add result |
|---|---|---|---|
| `0x3f4b9617a9a5a876` | `0x4085500000000000` / 682 | `0x3f4b990fc35d0000` | `0x3f4b990fc3725000` |
| `0x3ea73473ef62382d` | `0x4073600000000000` / 310 | `0x3ea734745e800000` | `0x3ea7347454000000` |
| `0x3f642dcd48c15028` | `0x4079000000000000` / 400 | `0x3f6434274b6dee00` | `0x3f6434274b710e00` |
| `0x3f307f0b9d772723` | `0x4074f00000000000` / 335 | `0x3f307f9348af0000` | `0x3f307f93489a1000` |

Large-period dispatch pins (`nominal_rate = 0.05`):

| `npery` bits | Truncated count | Selected route | Excel result bits |
|---|---:|---|---|
| `0x41efffffffc00000` | 4,294,967,294 | x87-DR LSB loop | `0x3faa403b3dfedfa0` |
| `0x41efffffffd80000` | 4,294,967,294 | x87-DR LSB loop | `0x3faa403b3dfedfa0` |
| `0x41efffffffe00000` | 4,294,967,295 | raw stored power chain | `0x3faa403b3ea009a0` |
| `0x41effffffff80000` | 4,294,967,295 | raw stored power chain | `0x3faa403b3ea009a0` |
| `0x41f0000000000000` | 4,294,967,296 | raw stored power chain | `0x3faa403b3ebaf340` |

### EFFECT rejected graph families

The evidence rejects an ordinary/publication-compatible `POWER` integer
path, native `powf`, raw `EXP(LN(base)*n)`, MSB-first binary exponentiation,
linear repeated multiplication, a single route across the `u32::MAX` boundary,
error guards at `2^53`/signed/unsigned 64-bit limits, and the tested
algebraically rearranged base forms. An x87 final subtract and an ordinary final subtract may be
observationally collapsed on portions of this positive domain; the identified
production graph uses `DR(acc - 1)` and the exact result pins above protect the
published behavior.

## RRI — identified guard, DAZ, identity, and raw-power graph

For finite scalar inputs, the complete current-reference graph is:

```
if periods < MIN_NORMAL:                         # includes zero/negative/subnormal
    return #NUM!

pv = DAZ(present_value)                          # subnormal -> signed zero
fv = DAZ(future_value)
if pv == fv:
    return +0                                    # before sign guards
if pv <= 0 or fv < 0:
    return #NUM!

base = DAZ(DR(fv / pv))
if base == 0:
    return -1
if base is nonfinite:
    return #NUM!

reciprocal = DR(1 / periods)
if reciprocal is nonfinite:
    return #NUM!

if periods == 1:
    powered = base                               # exact identity route
else:
    ln_base = LN_x87(base)                       # publish binary64
    product = DR(reciprocal * ln_base)           # reciprocal-first product
    powered = EXP_x87(product)                   # publish binary64

result = DR(powered - 1)
if result is nonfinite: return #NUM!
return result
```

`DAZ` means that every subnormal magnitude is observed as signed zero at the
specified boundary. The ordering is load-bearing: the period cutoff precedes
the equality route, while value equality precedes the sign guards. Thus equal
negative normal values return `+0`; zero or subnormal future values with a
positive normal present value return `-1`; and a positive subnormal period
returns `#NUM!` even when the values compare equal.

The `periods == 1` branch is an exact identity route, not the raw power chain:
it preserves `f64::MAX` and `MAX-1` exactly. The immediately adjacent period
doubles take the raw chain and publish different results. For every other
positive finite base, `RRI` uses the raw stored-log/product x87 power chain and
does **not** call the worksheet `POWER` wrapper.

This ordering is material near `future_value / present_value == 1`, where the
final subtraction magnifies a one-bit difference in `powered`. It is also
material at `periods = 2`: routing through worksheet `POWER` activates its
exponent-0.5 square-root shortcut and produces the wrong bits.

### RRI candidate scores and status correction

| Candidate | Banked grid | Fresh 4,900 held-out | 375-row follow-up |
|---|---:|---:|---:|
| raw reciprocal-first x87 `LN`/multiply/`EXP` | 154/154 | 4900/4900 | **375/375** |
| worksheet `POWER` wrapper | collapsed on this grid | 4900/4900 | 204/375 |
| native `powf` | — | 4705/4900 | 132/375 |
| `EXP(LN(base) / periods)` | — | 4803/4900 | 339/375 |

The complete composite additionally scores `60/60` on the first edge-domain
battery, `35/35` on a fresh disagreement battery, and `6/6` on the clean
period-one/adjacent-period discriminator. The former production guard/raw-chain
model scored only `45/60`, `15/35`, and `3/6` on those sets. Combined with the
four positive-domain corpora, the repaired production replay is `5536/5536`.

The initial 4900/4900 tie with `POWER` was a corpus-coverage false tie: the
held-out generator began its integer-period lane at 3 and therefore missed
the decisive exponent-0.5 dispatch. The follow-up changes the model status
from “POWER-compatible reciprocal product” to the raw chain above. This is an
important status drift and is why the present record does not rely on a score
alone without branch discriminators.

A four-row `b27D` product-order battery selected the reciprocal-first
double-rounded multiplication 4/4. The exact live results were:

```
0xbfef2a2e7e96d4e5
0xbfef2e21887b5a4e
0xbfef48c1e7522815
0xbfe6bc50cd435225
```

The ordinary product lost all four. `LN(base)/periods` also lost the fourth
row (`...5226` versus live/raw `...5225`).

### RRI raw-chain versus POWER pins

| `periods` | `base` (or `pv,fv`) | Excel/raw result | worksheet `POWER` route |
|---|---|---|---|
| 2 | `pv=1`, `fv=2` | `0x3fda827999fcef30` | `0x3fda827999fcef34` |
| `0x3fe0000000000000` (0.5) | `0x3ffaea0b8ab00060` | `0x3ffd4605145cf0a6` | `0x3ffd4605145cf0a8` |
| `0x3fd5555555555555` (about 1/3) | `0x400b450356df2b67` | `0x40434d9ee17ba519` | `0x40434d9ee17ba518` |
| `0x3fd0000000000000` (0.25) | `0x401e01040abb3a31` | `0x40a8b9793de74b43` | `0x40a8b9793de74b48` |

Near-one cancellation pins:

| `periods` | `pv` | `fv` bits | Excel result bits |
|---:|---:|---|---|
| 64 | 1 | `0x3ff0000100000000` | `0x3e4fffff00000000` |
| 16 | 1 | `0x3ff0000040000000` | `0x3e4fffffc0000000` |
| 4 | 1 | `0x3ff0000010000000` | `0x3e4ffffff0000000` |

The six-row wrapper-staging capture separately selected x87 double rounding
for quotient construction, reciprocal construction, and the final subtract,
2/2 per operation:

| Axis | Inputs (binary64 bits) | Excel/x87 result | ordinary result |
|---|---|---|---|
| quotient | `n=0x3fe6e006120d042e`, `pv=0x402978cc6ac1e168`, `fv=0x40233c61102a784a` | `0xbfd4ca3920945ee6` | `0xbfd4ca3920945eea` |
| quotient | `n=0x4005212d6e8139b0`, `pv=0x3fcab99943a5b3ab`, `fv=0x4004e632e21067d4` | `0x3ff9a5b86541f846` | `0x3ff9a5b86541f844` |
| reciprocal | `n=0x3fe8e568cfd0b2e3`, `pv=0x3fca61d325e4cc68`, `fv=0x4003de1b6b8eca5b` | `0x40378351f3b47272` | `0x40378351f3b47275` |
| reciprocal | `n=0x3fcbfcb653b0b35f`, `pv=0x4008495ceb04db83`, `fv=0x4030d4b519cf7924` | `0x40a3b424c968f2bf` | `0x40a3b424c968f2b5` |
| final subtract | `n=0x3fd139ecfdbe8f22`, `pv=0x4014ddff55ccc4ac`, `fv=0x3fd1fca822b3c00d` | `0xbfefffd76a65a154` | `0xbfefffd76a65a155` |
| final subtract | `n=0x3fc90ab8bd6cd61e`, `pv=0x402cfffb4faa7327`, `fv=0x3ff148ab7524aae2` | `0xbfeffffc6585a794` | `0xbfeffffc6585a793` |

### RRI guard/DAZ/identity pins

| Mechanism | Inputs | Excel result |
|---|---|---|
| subnormal period guard before equality | `n=MAX_SUB`, `pv=fv=1` | `#NUM!` |
| minimum-normal period admitted | `n=MIN_NORMAL`, `pv=fv=1` | `+0` |
| signed-zero equality before sign guard | `n=1`, `pv=+0`, `fv=-0` | `+0` |
| subnormal DAZ equality | `n=1`, `pv=MIN_SUB`, `fv=MAX_SUB` | `+0` |
| zero future | `n=1`, `pv=2`, `fv=+0` | `-1` |
| quotient DAZ from normal operands | `n=MAX`, `pv=2^53`, `fv=MIN_NORMAL` | `-1` |
| quotient at minimum normal | `n=MAX`, `pv=2`, `fv=2*MIN_NORMAL` | `+0` |
| exact-period identity | `n=1`, `pv=1`, `fv=MAX` | `0x7fefffffffffffff` |
| lower adjacent period uses raw chain | `n=0x3fefffffffffffff`, `pv=1`, `fv=MAX` | `0x7fefffffffffff2a` |
| upper adjacent period uses raw chain | `n=0x3ff0000000000001`, `pv=1`, `fv=MAX` | `0x7feffffffffffb2a` |

### RRI rejected graph families

The evidence rejects an unconditional raw power chain, the worksheet `POWER`
wrapper, native `powf`, division of the stored logarithm by `periods`, an
ordinary binary64 product, ordinary quotient/reciprocal/final-subtract wrapper
operations, non-DAZ value/quotient handling, a `periods <= 0` cutoff, and a
sign-before-equality guard order. The
4900-row false tie is retained in this report as a held-out-risk lesson rather
than being erased from the history.

## NOMINAL — identified two-route valid-numeric graph

After truncating `npery`, `NOMINAL` uses two distinct x87 power substrates:

```
n          = trunc(npery)
base       = DR(1 + effect_rate)                  # publish binary64
reciprocal = RN53(1 / n)

if n <= 2:
    powered = POW_x87_direct(base, reciprocal)    # one final binary64 store
else:
    ln_base = LN_x87(base)                        # publish binary64
    product = DR(reciprocal * ln_base)
    powered = EXP_x87(product)                    # publish binary64

delta  = RN53(powered - 1)
result = RN53(n * delta)
```

`POW_x87_direct` keeps the entire power calculation register-continuous:

```
t = FYL2X(reciprocal, base)       # reciprocal * log2(base), EXT80
k = FRNDINT(t)                    # EXT80 integer under the Excel x87 CW
f = t - k                         # EXT80
w = F2XM1(abs(f))                 # 2^abs(f) - 1
m = 1 + w
if f < 0: m = 1 / m
powered = FSCALE(m, k)
store powered once to binary64
```

Spilling the `FYL2X` product or its logarithmic inputs before the
`FRNDINT`/`F2XM1`/`FSCALE` assembly changes answers. Conversely, the raw route
for `n >= 3` deliberately publishes `LN_x87(base)` and the product before
`EXP_x87`.

The observed branch can equally be written `reciprocal >= 0.5`, because all
valid `NOMINAL` inputs first truncate `npery` to an integer `n >= 1`. Those two
predicates are observationally identical at this function boundary; the
report therefore identifies the public graph as `n <= 2` without claiming an
unobservable internal source predicate. `RRI` proves that a large reciprocal
exponent does not globally select this direct routine across financial
functions.

### NOMINAL candidate scores

| Candidate | 600-row boundary/follow-up | 242-row adjacent `n>=3` | Combined |
|---|---:|---:|---:|
| hybrid: direct x87 for `n<=2`, raw chain for `n>=3` | 600/600 | 242/242 | **842/842** |
| one raw chain for every `n` | 588/600 | 242/242 | 830/842 |
| `EXP(LN(base)/n)` | 588/600 | 203/242 | 791/842 |
| worksheet `POWER` | 542/600 | 242/242 | 784/842 |
| direct register-continuous x87 for every `n` | 600/600 | 178/242 | 778/842 |
| native `powf` | 542/600 | 125/242 | 667/842 |
| use untruncated `npery` | 150/600 | — | — |

Two direct-x87 variants that spilled either the power argument or the
logarithmic intermediate scored 597/600 on the follow-up set. Keeping the
completed power extended through subtraction scored 441/842; keeping the
whole tail expression extended scored 438/842. Those losses prove the
binary64 publication boundary immediately after the power operation. A
multiply-before-subtract rewrite (`n*powered - n`) also lost the targeted
final-order pins and scored 709/842 when paired with the raw candidate.

The reciprocal computation for an integer `n` and some ordinary-versus-x87
tail roundings were observationally collapsed in a 12-million-row valid-domain
offline search. The graph above records the production staging that reproduces
the live corpus; it does not manufacture an internal distinction where no
public input currently exposes one.

### NOMINAL route and staging pins

One same-effect branch pair isolates the route boundary:

```
effect_rate = 0x400bf137020fc250

n=2: Excel/direct = 0x4001e9f49f3f60d8
     raw chain     = 0x4001e9f49f3f60da

n=3: Excel/raw    = 0x3fff342fbb6b38db
     direct x87   = 0x3fff342fbb6b38d8
```

The eight-row wrapper-staging capture adds the following axes:

| Axis | `effect_rate` bits | `n` | Excel/selected result | Rejected result |
|---|---|---:|---|---|
| x87 base add, direct route | `0x3eb4b5bf2f080059` | 2 | `0x3eb4b5bec3c00000` | ordinary add `0x3eb4b5bec3e00000` |
| x87 base add, direct route | `0x3e5bc03275fff5c1` | 2 | `0x3e5bc03278000000` | ordinary add `0x3e5bc03270000000` |
| store base before direct power | `0x3d8683445358528c` | 2 | `0x3d86840000000000` | unspilled EXT base `0x3d86830000000000` |
| store base before direct power | `0x3f7aa803f3d0ccd0` | 2 | `0x3f7a9cf2ed8bec00` | unspilled EXT base `0x3f7a9cf2ed8bea00` |
| x87 base add, raw route | `0x3dc87a14003e7108` | 4 | `0x3dc87a0000000000` | ordinary add `0x3dc87a2000000000` |
| x87 base add, raw route | `0x3d81af400727aaf4` | 13 | `0x3d81ac0000000000` | ordinary add `0x3d81b28000000000` |
| subtract before multiply | `0x3eb4b5bf2f080059` | 959 | `0x3eb4b5be44200000` | `n*powered-n`: `0x3eb4b5be40000000` |
| subtract before multiply | `0x3e2329aa1001d534` | 327 | `0x3e2329a380000000` | `n*powered-n`: `0x3e2329a000000000` |

### NOMINAL rejected graph families

The evidence rejects a single raw route, a single worksheet-`POWER` route, a
single direct-x87 route, native `powf`, `LN(base)/n`, use of untruncated
`npery`, direct-power variants with intermediate spills, keeping the completed
power extended through the tail, carrying an unspilled extended base into the
direct routine, ordinary base addition, and `n*powered - n` final ordering.

## Witness and hash ledger

These hashes identify the answer files used for the scores above. “Contextual
20228” means the host profile was established by the contemporaneous live
runner, but was not serialized inside that `WitnessSet`.

| Function / corpus | Rows | Answer-file SHA-256 | Provenance state |
|---|---:|---|---|
| EFFECT banked grid | 315 | `AF40CD04C576D9D89D809387D1D3910805E322523AE7DAF60B720B6451910979` | banked; not current-host sign-off |
| EFFECT held-out | 870 | `64B42A8B394612FA90CB9C1711D4897970661D8241C1F251D30DF2E13EC7C732` | embedded 20228 x64/CV2/NoCache; recaptured |
| EFFECT wrapper staging | 4 | `A4A37216ADCB0EFC09D613F3261FF439C153E83D51C0462ED5AC3C7E798A28D6` | contextual 20228 x64/CV2/NoCache |
| EFFECT extreme-domain/dispatch | 160 | `EB7CBA416C3A4C7145A1661ADCEBC6D3A3FC7645750F2CAF0E7E8A592D8430C0` | embedded 20228 x64/CV2/NoCache |
| RRI banked grid | 154 | `7E721AABB3EBC7D6703EC22F452497CEC877739F762E50CFC3DBD7786CE40217` | banked; not current-host sign-off |
| RRI held-out | 4900 | `EDF5304E39855A04BCD4F75E6A6215EA34688F2CC6B0AF2B03AF1E03344E811D` | embedded 20228 x64/CV2/NoCache; recaptured |
| RRI follow-up | 375 | `2E84DD72CE91BEA8E3D485E17C1995D69B93337FD551EC9E0C091FC735A829F0` | embedded 20228 x64/CV2/NoCache; recaptured |
| RRI wrapper staging | 6 | `586CB779CAF698373E6C31D1F7F5C9DAFDD7B455C9414A176EDBD20B49688DF6` | contextual 20228 x64/CV2/NoCache |
| RRI edge-domain stage 1 | 60 | `40626DE8452BC87F8DC378CDF4CAD4C8CE03BB41EF8637EB2FB36E17C09AEB6F` | reproducibly materialized build20228 x64/CV2/NoCache typed outcomes |
| RRI blind edge disagreement | 35 | `52E11144FA0BC8E0CAE88BB7ACE1F7084173D2836ACD82AC3FD07CA70C171F83` | reproducibly materialized build20228 x64/CV2/NoCache typed outcomes |
| RRI exact-period discriminator | 6 | `7C751F7A0165377D9E8C23667C0FDA1BADC7DF574AD3687F717FC721069AF6EF` | clean serialized build20228 x64/CV2/NoCache live capture |
| NOMINAL adjacent `n>=3` | 242 | `32EB2557553A505E9DB35DCE8045F6B0EC730B3A403DEE73135D14FA38C94233` | embedded 20228 x64/CV2/NoCache; recaptured |
| NOMINAL boundary/follow-up | 600 | `39D909BE1E9396E4A75E32C0A77173A5D011445EF024E71D54996FC037261D66` | embedded 20228 x64/CV2/NoCache; recaptured |
| NOMINAL same-effect branch pair | 2 | `D8E15900936A4EE3B93DCFEDEAD7536F9290E65D10F8BC4A79CAC0B0312A6A47` | embedded 20228 x64/CV2/NoCache; recaptured |
| NOMINAL wrapper staging | 8 | `CFB9EEB1EB410B4E1121D1FFF459F1481A5219980B99DAEE853AF15F24C03186` | embedded 20228 x64/CV2/NoCache |

The RRI edge-artifact generator is deterministic:
`cargo run --quiet --bin race_effect_rri_check -- --write-rri-edge-artifacts`.
It reparses and asserts every id, argument bit tuple, typed outcome, and row
count. Batch hashes are `008045A3...F227FE` (60),
`A5E3E1F4...606BF` (35), and `37428EC7...1D94F` (6). The materialized answer
metadata records `captured_utc = null` because per-row timestamps were not
retained; it records the honest capture date, public-interface path, build,
bitness, CV, no-cache mode, and zero-process serialization context instead.

The serialized six-batch recapture verifier reproduced every requested row
against the selected production graphs. Across all banked, recaptured, and
staging sets, the current production replay is exact for:

```
EFFECT:  315 + 870 + 4 + 160 = 1349/1349
RRI:     154 + 4900 + 375 + 6 + 60 + 35 + 6 = 5536/5536
NOMINAL: 242 + 600 + 2 + 8   = 852/852
```

## Landed production and test state

Commit `876635e` contains the selected Rust routes and exact regression pins for
the three functions:

- `EFFECT`: x87-DR LSB-first integer loop below `u32::MAX`, raw stored power
  chain at/above the boundary, plus wrapper and extreme-domain pins;
- `RRI`: raw `excel_pow_chain` rather than `power_kernel` on every published-
  positive-base row except the exact `periods==1` identity route, plus the
  identified MIN_NORMAL period cutoff, DAZ/equality/sign ordering, zero-base
  `-1` route, exponent-0.5 and cancellation pins;
- `NOMINAL`: the direct-x87/raw hybrid, same-effect `n=2`/`n=3` boundary pins,
  stored-base/power-publication pins, and tail-order pins.

Landed-repair verification on 2026-08-09:

1. `effect_uses_x87_spill_binexp_on_banked_and_blind_discriminators`: passed.
2. `effect_switches_to_raw_pow_chain_at_u32_max_truncated_periods`: passed.
3. `rri_uses_raw_x87_pow_chain_and_x87_spill_wrapper`: passed.
4. `rri_matches_excel_daz_guard_order_and_exact_period_identity`: passed.
5. `nominal_uses_direct_x87_then_raw_pow_routes_with_stored_power`: passed.
6. `race_effect_rri_check`: EFFECT `1349/1349`, RRI `5536/5536`, and NOMINAL
   `852/852`, including exact typed edge outcomes.
7. Post-repair `cargo test --manifest-path crates/oxfunc_core/Cargo.toml`:
   library `1518 passed; 0 failed; 4 ignored`; every shown integration target
   and doc-test target passed.
8. `lake build` in `formal/lean`: passed (`492` jobs), including the W109
   EFFECT/NOMINAL route classifiers and ordered RRI wrapper alignment theorems.

## Closure reconciliation and remaining gates

1. BUG-FUNC-043/044/045 record `876635e` as the fixed ref and pass their scoped
   `OPERATIONS.md` Sections 12 and 14 audits. Their beads are closed, their
   calculation-map rows retain the historical graph/evidence with
   `closed_signed_off` status, and G6-12/G6-13/G6-14 are retired from the
   open-only discrepancy catalog.
2. No FEC/F3E boundary or evaluator-facing clause changed, so no cross-repo
   handoff is required for these repairs.
3. W109 remains `scope_partial`, `target_partial`, and only partially integrated
   because the wider catalog, fresh broad discovery, shared COS/BESSELJ,
   CONVERT, PMT-family, and other active lanes remain open. The global
   `OPERATIONS.md` Sections 12 and 14 audit belongs at the campaign exit gate,
   not to this three-bug closure.
