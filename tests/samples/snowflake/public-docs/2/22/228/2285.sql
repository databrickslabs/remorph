select k, stddev_samp(v), stddev_samp(v2) from aggr group by k;

---+----------------+-----------------+
 k | stddev_samp(v) | stddev_samp(v2) |
---+----------------+-----------------+
 1 | [NULL]         | [NULL]          |
 2 | 8.539125634    | 12.013880859    |
---+----------------+-----------------+