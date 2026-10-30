# GAMMA tiny-x reciprocal and subnormal admission (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject, cell-ref formulas.

Positive subnormals publish `#NUM!` (error type 6), matching published
GAMMALN. Min-normal `f64::MIN_POSITIVE` is admitted.

On admitted `0 < x <= 1e-16`, `GAMMA(x)` equals worksheet `1/x` bit-exactly:

- decade grid `1e-307 ..= 1e-16` (powers of ten)
- min-normal `0x7fd0000000000000`
- 27-point neighborhood of `1e-16` (16 ulps below through 1e-16 inclusive)

First probed miss: `2e-16` (1 ULP). Do not extend the cutoff.

Pins: `GAMMA(1e-16)=0x4341c37937e08000`, `GAMMA(MIN_POSITIVE)=0x7fd0000000000000`.

G3-02 remains open above `1e-16` and for `n>=89` / `n+0.5>=20.5`.
