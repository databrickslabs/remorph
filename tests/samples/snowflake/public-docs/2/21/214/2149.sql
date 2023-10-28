select k, regr_intercept(v, v2) from aggr group by k;

---+-----------------------+
 k | regr_intercept(v, v2) |
---+-----------------------+
 1 | [NULL]                |
 2 | 1.154734411           |
---+-----------------------+