# GAMMA k/d-1 peels in (-1,0) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject. Honest uint64 ULP.

Worksheet `GAMMA(x)=GAMMA(x+1)/x` is exact for:

- 7/12 of `x=k/13-1` (k=1,2,6,7,9,10,11). IEEE `GAMMA(1/13)/(1/13-1)`
  is 5 ULP from `GAMMA(1/13-1)`.
- 8/10 of `x=k/11-1` (k=2,3,5,6,7,8,9,10; k=1,4 miss 1 ULP).
- 5/16 of `x=k/17-1` (k=2,3,11,13,16).

Those residues are published-bit seeds. Misses stay generic.

Second peel into (-2,-1) from exact first-peel thirteenths is exact
for k=2,10,11 (3/7). k=1,6,7,9 miss 1-2 ULP.

Third peel into (-3,-2) from those three is exact 3/3.

Further 11ths peels: k/11-4 3/3, k/11-5 3/3, k/11-6 2/3 (k=2 misses),
k/11-7 1/2 (k=10 only). 10/11-8..10 miss; 10/11-11 is exact again.

Further published-bit (−1,0) seeds from landed (0,1) residues where
the worksheet peel is 1–4 ULP (not an identity): 3/7-1, 5/7-1, 5/16-1,
13/16-1, 5/9-1, 1/12-1, and 7/12-1 (x bits distinct from −5/12).

Second peel into (−2,−1) from those is exact for 3/7-2, 5/16-2, 13/16-2,
5/9-2, 7/12-2 (5/7). 5/7-2 and 1/12-2 miss. Third peel into (−3,−2) is
exact for 3/7-3, 13/16-3, 5/9-3 (3/5). Fourth peel into (−4,−3) is exact
for 3/7-4 and 13/16-4. Fifth peels miss 1 ULP.

Remaining seventeenth first peels k/17-1 for k=4,5,7,8,9,10,12,15 are
1–2 ULP from the worksheet peel and are published-bit seeds. Missing
eleventh/thirteenth first peels 1/11-1, 4/11-1, 3/13-1, 4/13-1, 5/13-1,
8/13-1, 12/13-1 likewise (1–3 ULP). Fifths 1/5-1..4/5-1, ninths 1/9,4/9,8/9,
tenths 1/10,7/10,9/10, 5/12-1, 11/12-1, and 3/16-1 are further published-bit
seeds (worksheet peels 1–3 ULP). Second peels of 1/5,2/5,3/5,4/5,1/9,4/9,7/10
into (−2,−1) are exact (7/12 of that batch). Third peels 2/5-3 and 3/5-3
are exact; 3/5-4 is exact; 2/5-4 misses 1 ULP. 4/17-2, 8/17-2, 9/17-2 are exact;
those third peels miss 1 ULP.
