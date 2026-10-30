# GAMMA(n+0.5) product-first through 171.5 (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`GAMMA(n+0.5)` for `n=0..=171` is the native product-first fold

`(0.5 * 1.5 * ... * (n-0.5)) * GAMMA(0.5)`

with seed `0x3ffc5bf891b4ef6b`. Worksheet `PRODUCT` of those terms
times `GAMMA(0.5)` is 172/172, and IEEE sequential product-then-seed
matches the same bits.

Stepwise `GAMMA(x)=(x-1)*GAMMA(x-1)` from 19.5 misses 20.5 (1 ULP).
Seed-first IEEE `GAMMA(0.5)*0.5*1.5*...` also misses 20.5.

`GAMMA(172.5)` is `#NUM!` (the product overflows).

This replaces the former `(2n-1)!!/2^n` closed form through 15.5 plus
recurrence through 19.5 with one product-first graph through overflow.
