SELECT k, COVAR_SAMP(v, v2) FROM aggr GROUP BY k;


---+-------------------+
 k | covar_samp(v, v2) |
---+-------------------+
 1 | [NULL]            |
 2 | 120               |
---+-------------------+