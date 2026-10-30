# GAMMA fifths and odd tenths in (0,1) (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject (`k/5` and `k/10`
constructed in-sheet).

Fifths seeds:

| x | GAMMA bits |
|---|---|
| 1/5 | `0x40125d0622505413` |
| 2/5 | `0x4001beca6e4dff14` |
| 3/5 | `0x3ff7d3bb4061b952` |
| 4/5 | `0x3ff2a0af5617b4b9` |

`GAMMA(1/5)` is 2 ULP from the generic path. Native recurrence
`GAMMA(x)=(x-1)*GAMMA(x-1)` already misses at n=1 (1 ULP) on all four
families (best later-exact 6/11 on 3/5). Seeds only; recurrence not
claimed.

Odd tenths seeds (even tenths are fifths or 1/2):

| x | GAMMA bits |
|---|---|
| 1/10 | `0x402306ea7b280d88` |
| 3/10 | `0x4007eebbb8aec4ab` |
| 7/10 | `0x3ff4c4d5ab21ea23` |
| 9/10 | `0x3ff1191a68f2b5e1` |

`GAMMA(1/10)` is 3 ULP from the generic path. Recurrence not claimed.
