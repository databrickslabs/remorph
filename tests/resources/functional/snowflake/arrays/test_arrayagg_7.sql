-- snowflake sql:
WITH cte AS (
  SELECT
    id,
    tag,
    SUM(tag:count) AS item_count
  FROM another_table
)
SELECT
id
, ARRAY_AGG(tag) WITHIN GROUP(ORDER BY item_count DESC) AS agg_tags
FROM cte
GROUP BY 1;

-- databricks sql:
WITH cte AS (
    SELECT
      id,
      tag,
      SUM(tag:count) AS item_count
    FROM another_table
  )
  SELECT
    id,
    TRANSFORM(
      ARRAY_SORT(
        ARRAY_AGG(NAMED_STRUCT('value', tag, 'sort_by_0', item_count)),
        (left, right) -> CASE
                                WHEN left.sort_by_0 < right.sort_by_0 THEN 1
                                WHEN left.sort_by_0 > right.sort_by_0 THEN -1
                                ELSE 0
                            END
      ),
      s -> s.value
    ) AS agg_tags
  FROM cte
  GROUP BY
    1;
