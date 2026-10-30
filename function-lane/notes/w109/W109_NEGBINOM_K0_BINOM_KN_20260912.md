# NEGBINOM.DIST(0,s,p) = BINOM.DIST(s,s,p) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject. Honest uint64 ULP.

`NEGBINOM.DIST(0,s,p,FALSE)=BINOM.DIST(s,s,p,FALSE)` 8/8. Worksheet
`POWER(p,s)` is 0/8 (1-16 ULP).

Production BINOM k=n already matches those Excel bits 8/8. NEGBINOM k=0
now dispatches through that BINOM kernel.
