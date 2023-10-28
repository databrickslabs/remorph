SELECT k, REGR_AVGX(v, v2) FROM aggr GROUP BY k;

---+------------------+
 k | regr_avgx(v, v2) |
---+------------------+
 1 | [NULL]           |
 2 | 22.666666667     |
---+------------------+