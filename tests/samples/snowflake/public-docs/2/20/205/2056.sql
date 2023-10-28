WITH states AS (
  SELECT approx_top_k(C4, 3, 5) AS state
  FROM lineitem
)
SELECT value[0]::INT AS value, value[1]::INT AS frequency
FROM states, LATERAL FLATTEN(state);

-------+-----------+
 VALUE | FREQUENCY |
-------+-----------|
     1 |    124923 |
     2 |    107093 |
     3 |     89438 |
-------+-----------+