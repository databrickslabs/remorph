select k, regr_sxy(v, v2) from aggr group by k;

---+-----------------+
 k | regr_sxy(v, v2) |
---+-----------------+
 1 | [NULL]          |
 2 | 240             |
---+-----------------+