# GAMMA(-0.5) and GAMMA(-1.5) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

`GAMMA(-0.5)` is **not** `-2*GAMMA(0.5)` with the positive half-integer seed
(1 ULP: Excel `0xc00c5bf891b4ef6a` vs `-2*0x3ffc5bf891b4ef6b`).

The one-step peel `GAMMA(-1.5)=GAMMA(-0.5)/(-1.5)` is bit-exact
(`0x4002e7fb0bcdf4f1`). Further negative halves are not a contiguous peel
family (11/16 exact, first miss `-2.5`).

Landed `-0.5` and `-1.5` only. G3-02 remains open.
