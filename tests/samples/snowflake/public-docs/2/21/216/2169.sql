select k, regr_avgy(v, v2) from aggr group by k;

---+------------------+
 k | regr_avgy(v, v2) |
---+------------------+
 1 | [NULL]           |
 2 | 20               |
---+------------------+