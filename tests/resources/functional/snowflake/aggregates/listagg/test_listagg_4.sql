-- snowflake sql:
SELECT col3, listagg(col4, ', ') WITHIN GROUP (ORDER BY col2 DESC)
FROM
test_table
WHERE col2 > 10000 GROUP BY col3;

-- databricks sql:
SELECT
  col3,
  ARRAY_JOIN(
    TRANSFORM(
      ARRAY_SORT(
        ARRAY_AGG(NAMED_STRUCT('value', col4, 'sort_by_0', col2)),
        (left, right) -> CASE
                                WHEN left.sort_by_0 < right.sort_by_0 THEN 1
                                WHEN left.sort_by_0 > right.sort_by_0 THEN -1
                                ELSE 0
                            END
      ),
      s -> s.value
    ),
    ', '
  )
FROM test_table
WHERE
  col2 > 10000
GROUP BY
  col3;
