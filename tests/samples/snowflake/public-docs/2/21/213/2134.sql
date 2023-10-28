select k, regr_sxx(v, v2) from aggr group by k;

---+-----------------+
 k | regr_sxx(v, v2) |
---+-----------------+
 1 | [NULL]          |
 2 | 288.666666667   |
---+-----------------+