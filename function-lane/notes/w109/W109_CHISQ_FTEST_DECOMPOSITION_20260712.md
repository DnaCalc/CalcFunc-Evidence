# W109: CHISQ.TEST & F.TEST decomposition (2026-07-12)

Both test functions were originally treated as "blocked on the G3-01
distribution substrate." Identity-decomposition probing identifies the
CHISQ.TEST statistic layer. For F.TEST, the original three-row decomposition
was later superseded by current-build evidence that separates a private
tail/publication route from the public FDIST/F.DIST surface.

## CHISQ.TEST / CHITEST (G3-05)

Proven on live bits, 4 contingency tables (2x2, 2x3, 2x5):

    CHISQ.TEST(obs, exp) == CHIDIST(S, df) exactly,  df = (r-1)(c-1)

where S is Excel's internal statistic. Probing CHIDIST at candidate S
bit-patterns (the tail cancels in the equality) pins S: on the two tables
whose CHIDIST tail is steep enough to be injective (df=4 large-stat; df=2
large-stat), the unique matching S is **offset 0 from the plain-double
ROW-MAJOR accumulation** `S = Σ_rows Σ_cols (o-e)²/e`. The flat-tail tables
(df=1, df=2 small-stat) are consistent (±1 ULP of S maps to the same
p-value bits, non-discriminating). => the statistic IS plain-double
row-major `Σ(o-e)²/e`; all CHISQ.TEST drift is inherited from CHIDIST.

## F.TEST / FTEST (G3-06)

The original July probe used three two-sample sets, with degrees of freedom up
to (5,6), and observed:

    F.TEST(a, b) == 2 · FDIST(F, df_hi, df_lo) exactly

where F = max(var_a, var_b) / min(var_a, var_b) with unbiased variances
(divisor n-1), df ordered (df of the larger-variance group, df of the
smaller). The factor 2 is exact for ordinary binary64 values. That three-row
observation is retained as historical evidence, but it was not discriminating
enough to establish a universal graph.

### Current-build correction (2026-08-09)

A design-for-divergence campaign on Excel 16.0 build 20228, x64, workbook
Compatibility Version 2 retracts the universal decomposition claim:

- a 48-row F.TEST discovery, 350 live FDIST candidate groups, and 96 live
  VAR.S companions yields corrected accepted-group histogram
  `{0:15, 1:32, 2:1}`;
- the best forward, stored-ratio variance model is only `32/48`, while the
  ratio formed from the two separately published VAR.S values is `28/48`;
- capturing the separately published direct F CDF does not change the 48-row
  result (`33/48` rows admit any external-tail-equivalent candidate);
- a retired 24-row exact-variance boundary battery scores only `15/24` even
  when the smaller of the live direct CDF and right tail is doubled; and
- a correctly oriented 3,975-row inverse-neighborhood refinement finds an
  exact external-FDIST-equivalence input on only `4/15` former no-hit rows.
  On the other 11 rows, consecutive nearby ratio inputs cross while skipping
  the F.TEST target bit pattern.

Thus Excel F.TEST has a private tail/publication graph that is observably
distinct from separately published FDIST/F.DIST on the residual surface. A
remaining private variance-schedule question is also open. The original
three-row equality is a valid bounded observation, not a function-wide
identity.

## Consequence

G3-05 remains a downstream consumer of the CHIDIST tail, and its statistic
layer remains identified. G3-06 cannot be closed merely by fixing the public
FDIST/F.DIST substrate: both its private F-tail/publication route and its
remaining variance schedule must be identified independently.

Corpora: G3-05-answers-chi-multi.json / -chidist-multi.json;
G3-06-answers-ftest.json / -fdist.json. Current-build correction and complete
artifact hashes: `FTEST_VARIANCE_DISCOVERY_CHECKPOINT_20260809.md` in the
tracked calc-graph research tooling.
