# W109 GAMMALN = LN(GAMMA) additional seeds (2026-09-12)

Live Excel 16.0 build 20326 / CV2 / 64-bit. Inputs via `Range.Value2`;
per-cell `Cells.Item` formulas; honest uint64 bit-distance.

Worksheet `GAMMALN(x)` equals worksheet `LN(GAMMA(x))` at further landed
GAMMA seeds beyond the earlier 1/5, 1/3, 1/7 (and 1/2 via the piecewise
kernel):

| x | GAMMALN bits | notes |
|---|---|---|
| 2/7 | `0x3ff25a9c12810ff0` | 4/7, 6/7 are not this graph |
| 3/7 | `0x3fe73e3996add6b2` | |
| 5/7 | `0x3fcf325cd39aec45` | |
| 3/8 | `0x3feb9e4d53fc3074` | 1/8, 5/8, 7/8 miss 1–10 ULP |
| 5/16 | `0x3ff0d8e1683cdcd1` | 1/16, 9/16 miss |
| 1/11 | `0x4002d0c317ddb0c0` | |
| 2/11 | `0x3ff9ff587e1ad8ce` | |
| 6/11 | `0x3fdf3ad24caad6dc` | other elevenths miss 1–24 ULP |
| 1/13 | `0x400433b1c2265eb7` | |
| 2/13 | `0x3ffcd17b700fc6c1` | |
| 1+1/13 | `0xbfa4549a42cb6665` | product-first GAMMA(14/13) |
| 2/17 | `0x4000a9daf888fcc2` | 1/17 is 1 ULP |
| 2.5 | `0x3fd2383e809a67e8` | half-integer product-first |
| 4.375 / 7.375 / 9.375 | see pins | 3/8 product-first, GAMMA n<=9 |
| 2.3125 | `0x3fc4b3a46906fd4c` | 5/16 product-first, GAMMA n<=4 |

Half-integers `n+0.5` with landed product-first GAMMA: worksheet
GAMMALN=LN(GAMMA) at n in
`{2,3,4,8,9,11,13,15,16,18,19,20,21,22,23,26,27,29,30,32,34,35,38,40,42,44,47,50,51,52,53,54,55,56,57,63,67,70,71,73,76,77,80,83,85,86,92,93,94,95,96,98,102,104,105,106,110,111,112,113,122,123,125,128,130,131,132,133,134,135,136,137,138,139,141,142,147,151,157,158,159,160,161,163,165,166,168,169,170}`
(89 values through 170.5). Neighboring halves miss 1 ULP.
`n=0` (x=0.5) already matches via the piecewise kernel.

Integers `n=4..=88` with reverse-product GAMMA: worksheet GAMMALN=LN(GAMMA)
at 41/86 values
`{4,5,6,7,13,18,19,20,21,22,23,24,25,26,27,29,31,32,37,39,41,44,48,49,51,53,58,59,60,64,65,67,72,76,77,78,79,84,85,86,88}`.
LN(FACT(n-1)) matches the same 41/86. n=3 and the complementary integers
miss 1–2 ULP.

Further product-first extensions of landed GAMMA slices (quarters n<=9,
eighths n<=9, sixteenths within nmax): 4.25, 5.25, 6.25, 7.25, 4.125,
6.125, 7.125, 9.125, 5.625, 7.625, 6.0625, 7.0625, 4.5625, 6.5625,
8.5625, 10.5625, 5.8125. Neighboring n miss 1–43 ULP.

Further nmax-bounded hits on 9/11, 10/11, 6/13, 7/13, 9/13, 7/17,
9/17, 10/17, 11/17, 5/9 (12/88 of a remaining-nmax scan).

Production publishes `excel_log(gamma_kernel(x))` at those x bits.
`GAMMALN(x+1)=GAMMALN(x)+LN(x)` is 0/10 on the same seed set (max 27 ULP)
and is not the graph.

CHIINV / `CHISQ.INV.RT(p,2)` vs worksheet `-2*LN(p)` is 17/18 (p=0.8 is
1 ULP). Alternate LN associations do not recover the miss. Not landed.
