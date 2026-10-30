# CHIDIST(df=1) / Gamma(1/2, scale=2) published-ERF identity

Date: 2026-08-18
Lane: W109 inverse-problem decomposition
Reference: Excel 16.0 build 20228, x64, Value2

## Status axes

- `execution_state`: `in_progress`
- `scope_completeness`: `scope_partial` (df=1 / Gamma(0.5,2) CDF route only)
- `target_completeness`: `target_partial`
- `integration_completeness`: `integrated` for the landed dispatch
- `open_lanes`: remaining G3-01 GRATIO/BRATIO body; ERF/ERFC.PRECISE body;
  GAUSS/NORMSDIST residual inherited from that body after the G-F3 / G-A400
  wrapper (`W109_NORMSDIST_GF3_WRAPPER_20260821.md`); BINOM CDF leftover vs
  BETA (implied-x is 1-p ±1 ULP on most misses); Poisson PMF duals not exact;
  even-df Poisson-series association; CHISQ.TEST statistic for df≠1

## Method

Related worksheet functions were asked, through cell `Range.Value2` inputs,
which public identity Excel actually computes. No Excel binary was inspected.

## Identities that survived a 154-row nonnegative bank

The bank is powers of two from `2^-60` through `2^4`, a 0.05-step grid
through 4, and the usual chi-square critical values up to 100, plus 0.

| Identity | Exact |
|---|---:|
| `CHIDIST(x,1)` = `ERFC.PRECISE(SQRT(x/2))` | 154/154 |
| `CHIDIST(x,1)` = `CHISQ.DIST.RT(x,1)` | 154/154 |
| `GAMMA.DIST(x,0.5,2,TRUE)` = `ERF.PRECISE(SQRT(x/2))` | 154/154 |
| `CHISQ.DIST(x,1,TRUE)` = `GAMMA.DIST(x,0.5,2,TRUE)` | 154/154 |
| `CHIDIST(x,1)` = `ERFC.PRECISE(SQRT(x)/SQRT(2))` | 123/154 (refuted) |
| `CHIDIST(x,1)` = `ERFC.PRECISE(SQRT(x)*(1/SQRT(2)))` | 117/154 (refuted) |
| `CHIDIST(x,1)` = `1-GAMMA.DIST(x,0.5,2,TRUE)` | 92/154 (cancellation, not the graph) |

The surviving staging is divide-by-two first, then worksheet `SQRT`.
`ERF`/`ERFC` and the `.PRECISE` aliases were bit-identical on a separate
16-point probe of this build.

## What was landed

`chisq_dist_rt_kernel` (CHIDIST / CHISQ.DIST.RT) and the cumulative
`chisq_dist_kernel` / `gamma_dist_kernel(x, 0.5, 2, TRUE)` now call the
published ERF/ERFC kernels at `sqrt(x/2)`.

On the same 154 Excel rows, before the dispatch OxFunc CHIDIST matched
63/154 (max 30 ULP). The ERFC composition matched 88/154 (max 31 ULP).
The dispatch is the identified graph; it also improves the current residual.
The remaining misses are the still-open ERF/ERFC.PRECISE body.

## Follow-up identities (2026-08-18, same build)

A second 68-row bank plus an 11-row CDF complement check:

| Identity | Exact |
|---|---:|
| `CHIDIST(x,2)` = `EXP(-x/2)` | 68/68 |
| `CHIDIST(x,2)` = `EXP(-(x/2))` | 68/68 |
| `CHISQ.DIST(x,2,TRUE)` = `1-EXP(-x/2)` | 9/11 (refuted as the CDF graph) |
| `GAMMA.DIST(x,0.5,1,TRUE)` = `ERF.PRECISE(SQRT(x))` | 68/68 |
| `GAMMA.DIST(x,0.5,4,TRUE)` = `ERF.PRECISE(SQRT(x/4))` | 68/68 |
| `CHIDIST(x,4)` = `EXP(-x/2)*(1+x/2)` | 50/68 (refuted) |
| `CHIDIST(x,6)` = next Poisson term | 46/68 (refuted) |

Landed: df=2 right-tail through `excel_exp(-(x/2))`; `GAMMA.DIST` CDF at shape `0.5` through `ERF.PRECISE(SQRT(x/beta))` for any positive finite scale.

## Follow-up identities (2026-08-19)

| Identity | Exact | Action |
|---|---:|---|
| `CHISQ.DIST(x,2,TRUE)` = `EXPON.DIST(x/2,1,TRUE)` | 85/85 | Landed |
| `CHISQ.DIST(x,2,TRUE)` = `GAMMA.DIST(x,1,2,TRUE)` | 85/85 | Same graph |
| `GAMMA.DIST(x,1,beta,TRUE)` = `EXPON.DIST(x/beta,1,TRUE)` | 85/85 dyadic; 11/11 for beta=3,5 | Landed (divide-first) |
| `EXPON.DIST(x,1/beta,TRUE)` | 1 ULP misses when 1/beta inexact | Refuted as the Gamma staging |
| `GAMMA`/`EXPON` PDF | 33/85 | Refuted |
| `CHIDIST(x,2)` = `POISSON.DIST(0,x/2,TRUE)` | 45/45 | Same as EXP |
| `CHIDIST(x,4)` = `POISSON.DIST(1,x/2,TRUE)` | 45/45 | Poisson CDF now dispatched (see 2026-08-19) |
| `CHIDIST(x,6)` = `POISSON.DIST(2,x/2,TRUE)` | 45/45 | Same |
| `CHIDIST(x,4)/EXP(-x/2)` = `1+x/2` | 70/85, leftover ±1–7 ULP | Series association still open |
| `ERFC.PRECISE(z)` = `CHIDIST(2*z*z,1)` | 27/27 | Implied Q is the published ERFC surface; no separate body |

General even-df rule observed: `CHIDIST(x, 2(k+1))` = `POISSON.DIST(k, x/2, TRUE)`.

## Poisson CDF landing (2026-08-19)

A 70-pair bank (`k ∈ {0,1,2,3,5}`, mixed `μ`) on live Excel 16.0 build 20228:

| Identity | Exact |
|---|---:|
| `POISSON.DIST` = `POISSON` alias | 70/70 |
| `POISSON.DIST(k,μ,TRUE)` = `CHIDIST(2*μ, 2(k+1))` | 70/70 |
| same with `μ*2` and `μ+μ` | 70/70 |
| `CHISQ.DIST.RT(2*μ, 2(k+1))` | 70/70 |
| `1-GAMMA.DIST(μ,k+1,1,TRUE)` | 45/70 (refuted) |
| sum of published `POISSON.DIST(j,μ,FALSE)` for `j=0..k` | 45/70 (refuted; only `k=0` is 14/14) |

Landed `poisson_dist_kernel` CDF as `EXP(-μ)` for `k=0` and GRATIO `Q(k+1, μ)` for `k≥1`, which is CHIDIST internals after the exact `2μ/2` recovery. The PMF path is unchanged.

## Follow-up identities (2026-08-19, continued)

Poisson PMF is **not** a CDF/CHIDIST difference (19/65) and **not** `EXP(-μ)*μ^k/FACT(k)` (23/65, only `k=0` is exact). Odd-df `CHIDIST(x,3)` is **not** a worksheet `ERFC+EXP` recurrence (best 15/47).

Cross-family CDFs that did latch:

| Identity | Exact | Action |
|---|---:|---|
| `CHISQ.DIST(x,df,TRUE)` = `GAMMA.DIST(x,df/2,2,TRUE)` | 88/88, df in 1..10 | Chi CDF now routes through `gamma_dist_kernel` |
| `1-CHIDIST` as chi CDF | 49/88 | Refuted |
| `NEGBINOM.DIST(f,s,p,TRUE)` = `BETA.DIST(p,s,f+1,TRUE)` | 150/150 | Landed through `regularized_beta` |
| `1-BETA` / `BETA(1-p,f+1,s)` | 1/8 | Refuted |

## Cross-family identities (2026-08-20)

Same method on a different set of functions, then applied back.

| Identity | Exact | Action |
|---|---:|---|
| `FISHER(x)` = `0.5*LN((1+x)/(1-x))` | 33/33 | Landed through `excel_log` of the combined ratio |
| `FISHER` = `ATANH` | 21/33 | Refuted; ATANH keeps a cubic small-x body |
| `FISHER` = `0.5*(LN(1+x)-LN(1-x))` | 10/33 | Refuted |
| `FISHERINV(y)` = `(EXP(2*y)-1)/(EXP(2*y)+1)` | 27/27 | Landed through `excel_exp` |
| `FISHERINV` = `TANH` | 10/27 | Refuted |
| `FISHERINV` = `1-2/(EXP(2*y)+1)` | 9/27 | Refuted (association) |
| `CHISQ.INV(p,df)` = `GAMMA.INV(p,df/2,2)` | 63/63 | Landed; endpoints `p=0 -> 0`, `p=1 -> #NUM!` also match |
| `CHIINV` = `CHISQ.INV.RT` | 63/63 | Alias |
| `CHISQ.INV.RT` = `GAMMA.INV(1-p,df/2,2)` | 34/63 | Refuted (1-minus) |
| `CHISQ.INV(p,2)` = `-2*LN(1-p)` | 24/36 | Refuted (closed form is not the inverse graph) |
| `LOGNORM.DIST` = `NORM.S.DIST((LN(x)-μ)/σ)` | 45/45 | Landed LN site as `excel_log` |
| `LOGNORM.DIST` = `NORM.DIST(LN(x),μ,σ)` | 45/45 | Same composition |
| `LOGNORM.INV(0.5)` = `EXP(NORM.INV(0.5))` | 45/45 | Landed EXP site as `excel_exp` |
| `NORM.DIST` = `NORM.S.DIST((x-μ)/σ)` | 45/45 | Already the local graph |
| `ACOSH(x)` = `LN(x+SQRT(x*x-1))` | 29/29 including 1+1ulp via Value2 array | Landed; `x*x` overflow `#NUM!` as in ASINH |
| `ACOSH` via `SQRT((x-1)*(x+1))` | 18/24 | Refuted |
| `WEIBULL(x,1,β)` = `EXPON(x/β,1)` | 22/24, 2 ULP | Not landed; WEIBULL keeps its own x87 body |
| `BINOM.DIST` CDF = `BETA.DIST(1-p,n-k,k+1)` | 135/150, leftover 1–4 ULP | Not landed; Value2 `q=1-p` does not close the misses |
| `BINOM.INV` = `CRITBINOM` | 27/27 | Alias |
| `TINV` = `T.INV.2T` | 27/27 | Alias |
| `FINV` = `F.INV.RT` | 27/27 | Alias |
| `STANDARDIZE` = `(x-μ)/σ` | 16/16 | Already the local graph |
| `PHI` = `NORM.S.DIST` pdf | 14/14 | Already closed |
| `GAUSS` = `0.5*ERF(x*SQRT(0.5))` | 13/14; sole miss `x=1e-8` | Tiny-x body still open |
| `ASINH` = `LN(x+SQRT(x*x+1))` | 6/10 unsigned | Misses negatives |
| `ASINH` = `SIGN(x)*LN(ABS(x)+SQRT(x*x+1))` | 23/23 Value2 array | Landed; `x*x+1` overflow uses `LN(2*|x|)` |
| `ASINH` = `SIGN*LN(ABS+HYPOT)` | 0/23 | Refuted as the worksheet graph |

## Lateral evaluation-tree pass (2026-08-21)

Clean-room ideas beyond “ask which public function it is”:

1. **Dual of a landed CDF identity.** If `POISSON.DIST(k,μ,TRUE)=CHIDIST(2μ,2(k+1))`, the PMF might be the corresponding gamma/chi *pdf*. It is not: `GAMMA.DIST(μ,k+1,1,FALSE)` and `2*CHISQ.DIST(2μ,2(k+1),FALSE)` are 15/48; `EXP*POWER/FACT` is 21/48.
2. **Implied-argument inversion.** Invert the near-identity and read the hidden `x` Excel fed the public kernel. `BETA.INV(BINOM.DIST(k,n,p,TRUE), n-k, k+1)` equals `1-p` on 89/125; 27 of 36 misses are ±1 ULP on `1-p` (often `nextafter(1-p,0)`). A handful are hundreds to millions of ULP, so BINOM is not a stored-`q` wrapper of `BETA.DIST`. Same pattern on `F.DIST` implied-z (20/45, 17 of 25 misses 1 ULP).
3. **Helper-cell staging.** Materialize `x*SQRT(0.5)` before `ERF`. Did not close GAUSS (13/22, same as the inlined tree).
4. **Cancellation-avoiding sibling.** `GAUSS(x)` is `NORMSDIST(x)-0.5` except where that subtraction underflows (dyadic |x| ≤ 2^-49). On dyadic |x| ≤ 2^-50, `GAUSS(x)=x*PHI(0)` bit-exactly. At 2^-49 the mantissa is quantized (`0x3cc8000000000000`). Tiny-x body still open.
5. **Signed vs unsigned public form.** ACOSH taught `LN(x+SQRT(x*x-1))`. ASINH needs the `SIGN/ABS` wrapper; the unsigned LN form is the negative-x failure mode (12/23).
6. **RANGE as a window on a CDF.** `BINOM.DIST.RANGE(n,p,0,k)=BINOM.DIST(k,n,p,TRUE)` 125/125 — same surface, not a new graph.
7. **Odd-df leftover as ERFC plus one published term** with helper `z=x/2`, `s=SQRT(z)`: 1–4/10, leftover 1–5 ULP. Not landed.

`BINOM.DIST.RANGE` matching the CDF is useful once the CDF graph is identified; it does not by itself identify it.

BINOM CDF argument-order was the Negbinom lesson applied back: the public beta
form is the right *shape* (`I_{1-p}(n-k,k+1)`), but Excel's BINOM surface is
not the published `BETA.DIST` / `NEGBINOM.DIST` kernel (15 leftover 1–4 ULP
rows, unchanged when `1-p` is written as Value2).

## What this is not

- Not a full G3-01 or G4-04 closure.
- Not an ERF coefficient identification.
- Not a claim about `GAMMA.DIST` at other shapes/scales.
- Not a BINOM CDF landing: the beta form remains a near-identity only.
- Not a GAUSS landing: `NORMSDIST-0.5` / `x*PHI(0)` split is characterized, not dispatched.
