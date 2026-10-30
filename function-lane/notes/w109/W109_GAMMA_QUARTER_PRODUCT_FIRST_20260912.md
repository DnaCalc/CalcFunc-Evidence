# GAMMA(n+1/4) product-first through 9.25 (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`GAMMA(n+1/4)` for `n=0..=9` is the native product-first fold

`(0.25 * 1.25 * ... * (n-0.75)) * GAMMA(0.25)`

with seed `0x400d013fc47eeeec`. Contiguous exact through 9.25; first
miss 10.25 (1 ULP). Seed-first recurrence from that seed misses 6.25.

`GAMMA(n+3/4)` product-first already misses 2.75, so that family stays
on the landed seed-first recurrence `n=0..=5`.
