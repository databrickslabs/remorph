select k, regr_syy(v, v2) from aggr group by k;

---+-----------------+
 k | regr_syy(v, v2) |
---+-----------------+
 1 | [NULL]          |
 2 | 200             |
---+-----------------+