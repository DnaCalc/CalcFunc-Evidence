# GAMMA odd-eighth product-first through n=9 (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

Product-first `(seed_frac * (1+seed_frac) * ... ) * GAMMA(seed)` is
contiguous exact for:

- `n+1/8` n=0..=9 (through 9.125; first miss 10.125)
- `n+3/8` n=0..=9 (through 9.375; first miss 10.375)
- `n+5/8` n=0..=9 (through 9.625; first miss 10.625)

`n+7/8` product-first already misses 1.875; keep the seed only.

This extends the former recurrence ranges (n<=3 / n<=3 / n<=2 / seed).
