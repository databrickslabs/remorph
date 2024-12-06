-- snowflake sql:
SELECT
  col2,
  ARRAYAGG(col4) WITHIN GROUP (ORDER BY col3, col5)
FROM test_table
WHERE col3 > 450000
GROUP BY col2
ORDER BY col2 DESC;

-- databricks sql:
 SELECT
    col2,
    TRANSFORM(
      ARRAY_SORT(
        ARRAY_AGG(NAMED_STRUCT('value', col4, 'sort_by_0', col3, 'sort_by_1', col5)),
        (left, right) -> CASE
                                WHEN left.sort_by_0 < right.sort_by_0 THEN -1
                                WHEN left.sort_by_0 > right.sort_by_0 THEN 1
                                WHEN left.sort_by_1 < right.sort_by_1 THEN -1
                                WHEN left.sort_by_1 > right.sort_by_1 THEN 1
                                ELSE 0
                            END
      ),
      s -> s.value
    )
  FROM test_table
  WHERE
    col3 > 450000
  GROUP BY
    col2
  ORDER BY
    col2 DESC NULLS FIRST;
