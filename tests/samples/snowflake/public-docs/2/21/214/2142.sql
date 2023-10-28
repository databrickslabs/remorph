select k, regr_slope(v, v2) from aggr group by k;

---+-------------------+
 k | regr_slope(v, v2) |
---+-------------------+
 1 | [NULL]            |
 2 | 0.831408776       |
---+-------------------+