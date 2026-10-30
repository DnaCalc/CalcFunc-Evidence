# W109 primitive-recovery campaign — RESUME DOC (2026-07-18)

Cold-restart state for the G3-01/G3-02 campaign. Full history: the two
identification notes (W109_G3-01_GRATIO_IDENTIFICATION_20260716.md,
W109_GAMMALN_IDENTIFICATION_20260711.md), the catalog rows, and the field
diary (docs/notes/CHOPPED_EXP_IDENTIFICATION_STORY.md). Work dirs
(gitignored): smart-fuzzer/work/w109/G3-01-dist/ and G3-02-gamma/ (agent
files prefixed agentA..R by lane; batteries batch-*/answers-* b1..b26).
Oracle: Run-W109BulkBatch.ps1 (~8,800 probes/s, one Excel instance —
serialize captures). STRICT BLACK-BOX policy (AGENTS.md Clean-room Rule):
no binary inspection, ever; oracle behavior + published sources only.

## IDENTIFIED + LANDED (production, committed through 6f01b96)

| What | Identity | Landed as | Evidence grade |
|---|---|---|---|
| Internal ln | fyl2x chain RN53 == CR everywhere probed | (callers use CR-equal std/chain) | proven 2 ways (LOGNORM RN-exact; cross-view solve) |
| Internal exp | x87 F2XM1 chain (naive y−round(y) reduction, PC=64), SITE-DEPENDENT publication: RN53 wrapper/pdf, RZ53 (chop) series r-site, extended delivery on erf path | excel_exp / excel_exp_rz (excel_numeric); all 49 substrate sites | **34,000/34,000 held-out (POISSON) — sign-off grade** |
| Internal expm1 | Kahan correction in DOUBLE: u=chain-exp(t); t if u==1; (u−1)·t/ln(u) if |t|<1; else u−1 (msvcr100 exports no expm1) | excel_expm1_internal; EXPON/WEIBULL cdf + a==1 wrapper | 17,996/18,000 (99.978%) |
| Gamma substrate | GRATIO (TOMS 654) plain-double SSE2; a==1 dispatch (−expm1(−x), exp(−x)); Cephes-form forward gser + (r/a)·ans + exact-factorial normalizer + chop-exp r | regularized_gamma_p/q | family EXHAUSTED, held-out-confirmed; ceiling = 2 microdetail walls (below) |
| Beta substrate | BRATIO (TOMS 708); accurate-complement wrapper stagings (FDIST x=d2/den y=d1F/den; T-family x=df/den y=t²/den) | bratio + wrappers + TTEST | bit-identity to spec 20,008/20,008; b22 held-out 285/655 |
| *INV inverters | fully-converged float-lattice bisection publish-hi, rooting the PUBLISHED surface (CHIINV→Q, FINV→complement form, TINV→2t) | bisect_inverse + kernels | b14+b19 held-out validated |
| Published GAMMALN | Cody-1967 FORM SET, thresholds retuned: x<0.7(exact double) composed −log(x)+core(x+1); B1 [0.7,1.5); B2 [1.5,4) x87-spill; B4=[4,8) published SPECFUN P4/Q4 x87-continuous (worst 1); x≥8 ONE Stirling formula (q=(x−0.5)log x−x+LS2PI; fdlibm w1..w6 vector, plain double) 99.83% worst 2 | excel_numeric/gammaln.rs → GAMMALN/GAMMALN.PRECISE | port bit-identical to ref on 17,003 rows; held-out 79.0% worst 5 |
| Distribution pow | exp(RN53(RN64(y·ln x))) — POWER's chain WITHOUT the 0.5→sqrt shortcut (shortcut is the POWER wrapper's, not the CRT pow's) | excel_pow_chain (excel_numeric); excel_pow_positive delegates | b24 re-race 33,145/33,145 (real chain); b27D product staging 113/113 |
| WEIBULL.DIST | legacy x87 per-op-DR body: r=DRdiv(x,β); t=pow_chain(r,α); cdf=−expm1(−t); pdf=`α/pow(β,α)*pow(x,α−1)*exp(−t)` LEFT-TO-RIGHT, every op DR-spilled (T3\|SS 1,600/1,600) | weibull_dist_kernel | **b28 held-out 5,999/6,000 = 99.983%** (sole miss = wall-1 class) |
| EXPON.DIST | same x87 per-op-DR body class: λ·x and pdf λ·e both DR (b28b 14/14+24/24) | expon_dist_kernel | **b28c held-out 4,000/4,000 = 100.000%** |
| Internal lgamma | EXTENDED precision, sub-ULP from CR, E_g nearest; distinct from published GAMMALN | (normalizer via exact factorial at integer a) | b24 GAMMA-window reads |

Corpus scores after all landings (lane-3 re-verified 2026-07-18, production
routing ≡ identified substrate bit-for-bit; both OxFunc-side integer-shape
fast paths REMOVED — they were silently overriding the identified kernels,
gamma one catastrophically at ±4,400 ULP): CHIDIST 152/195, GAMMA.DIST
modern 337/446, b26 integer-a 1,615/4,100 (worst −10), beta b22 293/671,
GAMMALN held2 314/400 + fresh-b32 b2 549/1,200 (B2 continuous re-landing:
+25 aggregate over all 1,554 b2 rows), BETAINV 12/30 worst +5, POISSON k=0
34,000+ consecutive exact, WEIBULL b28 5,999/6,000, EXPON b28c 4,000/4,000.
Suite 1,509 green.

## OPEN WALLS (each with banked per-row residuals + designed next probe)

1. **Chain-microdetail ±1 on series r** (the 7/45 class; some rows near tiny
   F2XM1 fractions): idealized == hardware == 38/45; inconsistent ±1 needed.
   Probe: dissect the 7 rows' chain internals op-by-op vs implied-r bits
   (agentQ_diag7.py started). Same class: 3/30k POISSON + 4/18k expm1 rows.
2. **ln-amplification wall at a≥3** (b26: worst grows 4→7→10 with a): a·L
   staging delivers CR-L; Excel's L may differ sub-ULP (extended L into a·L?
   — but extended-t1 REFUTED at a=2 with ±17; test a-dependent delivery).
3. **erf 190-path** (parked, resting state agentJ_resting_state.json): C10r
   composite 67.65%; the 1.01/0.505-pub-ULP equidistributed component with
   grid ∝ 2^Ez has ALL raced sources refuted. Probes: (i) find the 2^Ez-grid
   source, (ii) repair j-pipeline park phases at e=−15/−20 vs banked
   residuals, (iii) parked-vs-register-continuous chain floor.
   **b9heldout (256 rows) NEVER RACED — the promotion gate.**
4. **bgrat body op-graph** (parked; agentM: 53-bit, per-op-DR AND
   register-resident families ALL falsified by shared-z group-intersection;
   normalizer algdiv-class proven; GRATIO-sub q > grat1 in all combos).
   Probes: differential z-pairs (±1-2 ULP), flip-bracketing at bimodal
   a-positions, b→1⁻ sweep.
5. **GAMMALN b1/b2** — lane-4 outcome (2026-07-18, agent-S + fresh b32
   gate): **B2 re-landed CONTINUOUS x87 + LM coefficients** (fresh 549 vs
   518/1,200; same op-graph class as B4). **B1 = confirmed op-graph wall**:
   published-1967/plain-double is the held-out optimum of the whole
   enumerated staging family; misses to −3.4 ULP pre-round. Remaining
   probes (agentS_results.md §7): two-step argument reductions,
   re-weighted-Remez coefficient family, outer 2-op mask post-e/e/e-refit.
6. **POISSON k≥1 + BINOM/NEGBINOM routes** — REFRAMED by lane 2
   (2026-07-18; old "direct product proven / 21%" verdict WITHDRAWN —
   route-blind k=0 window):
   - POISSON pmf: k=1 = extended-composed direct product (exact at large
     λ); k≥2 = **Loader saddle-point dpois bit-exact at λ≳14**; small-λ
     staging + branch structure open.
   - **BINOM: IDENTIFIED AND LANDED (lanes 5–8b, 2026-07-18, commit
     85e91e4).** Production pmf = R dbinom_raw with THREE recovered source
     details: lc grouping `((s(n)−s(k))−(s(n−k)+bd0(k,np)))−bd0(n−k,nq)`
     (O3, 403/475 flips zero-false-positive); lf = `(M + ln k) +
     (ln(n−k) − ln n)` (log1p ported as TWO SEPARATE LNS — msvcr100 has no
     log1p, the expm1 hole again); arg = lc − 0.5·lf at RN64 EXTENDED into
     the fFEXP chain (`excel_binom_pmf_exp`); R bd0 (series thr 0.1;
     direct = single-ln x·L + (np−x)); stirlerr CR table + R tiers
     (constants machine-generated, agentU_gen_consts.py); Loader k=0/k=n
     branches (p<0.1 → exp(−bd0(n,nq)−np) else excel_pow_chain).
     Scores: b29 8.76→49.81%, b34 52.17%, b35 75.51%, FRESH b36 gate
     49.59% overall (k=n 96.4%, k=0 81.6%, general-k 37.9% with QUANTIFIED
     n-dependence — perfect ≤15, degrades >35). Row OPEN: (i) the 72/475
     second lc-flip source (DR-quotient rows suspect); (ii) small-operand
     bd0-direct smooth bodies (±0.2–2·2⁻⁵³, n-scaling measured by b36);
     (iii) NEGBINOM does NOT inherit (10.4% raced) — own route hunt.
     Chain EXONERATED (matched-argument b35 proof); reduction subtract
     always Sterbenz-exact; tbyte park transparent; PC53 refuted;
     fdlibm-poly-exp ties the chain on this data.
     Instruments: absolute-interval bank agentT_intervals_abs.json (31,200
     rows, zero-chain-call racing), matched-argument battery design
     (agentT_b35_gen.py), x87_serve op family (cexpext2*, lp1/FYL2XP1,
     lnext, bd0dir), check_binom_prod racer. Full ledgers:
     agentT_results.md (rounds 1–6) + agentU_results.md.
7. ~~Distribution pow staging~~ **CLOSED 2026-07-18 (lane 1)** — see the
   IDENTIFIED table; clue trail in W109_WALL_CLUES_LEDGER.md.
8. **BETA.DIST integer-shape fast path + A/B-bounds staging** (small probes,
   unmeasured).

## METHOD RULES (hard-won, do not relearn)

- NEVER call residuals "noise" — deterministic per-argument signal;
  distributions are class constraints; bank per-row values.
- Race DIRECTED-ROUNDING publications, not just nearest (the chop lesson).
- A period from a dense scan is real only if reproduced at a 10× finer grid
  (the b18 aliasing lesson); phase-gradients are the alias-free fingerprint.
- Tiny-y/high-a gamma rows are ln-amplification tests, not series tests.
- Held-out gates before promotion, always (MINVERSE lesson). Generate
  constant tables programmatically (the hand-conversion lesson).
- Captures serialized through one Run-W109BulkBatch.ps1 at a time.
- x87 emulation: mpmath workprec(64) RN per op then float(); real hardware
  via excel_numeric ext ops (parking through tbyte is transparent).

## KEY TOOLING

- Racers (calc_graph_racer bins): check_x87exp(_ext), check_gratio_prod,
  check_bratio, check_inv, check_exp_rd, check_gammaln_port, check_erf190,
  check_pow_dist, check_weibull_pdf, check_weibull_prod, check_expon_prod.
- **x87_serve + x87client.py (G3-01 work dir)**: line-oriented op server
  (exp/expz/ln/expm1/mul/div/recip/cexpext on real hardware) + Python batch
  client — arbitrary candidate op-graph exploration without new Rust bins.
  The tree×spill-mask enumeration template is lane1_pdf_round6.py.
- **W109_WALL_CLUES_LEDGER.md**: running clue trail for the walls, updated
  every lane.
- Scorers in work dirs: score_b22.py, agentQ_lib.py, agentL_composite3.py,
  agentJ_transfer.py (build/gate/hyp/invert), rdexp_race.py.
- Oracle cache shared; b9heldout + b26X reserved unraced.
