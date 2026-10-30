# Z.TEST omitted-sigma graph (2026-09-12)

Live Excel 16.0 build 20326 / CV2, Range.Value2 inject.

With omitted sigma, `Z.TEST(array, x)` equals

`NORMSDIST((x - AVERAGE(array)) / (STDEV.S(array) / SQRT(n)))`

bit-exactly on two independent datasets. `STDEV.P` is not the graph.
`1-NORMSDIST((mean-x)/se)` is not the graph (NORMSDIST complements are not
`1`).

Supplied sigma uses the same `z=(x-mean)/(sigma/√n)` graph
(`Z.TEST({1,2,3,4,5},4,2)=0x3febc87d3294a339`).

Production now routes through `norm_s_dist_kernel` with that `z`. G3-01
still open for remaining distribution last-bit.
