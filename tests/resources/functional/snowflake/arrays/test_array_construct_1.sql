-- snowflake sql:
WITH users AS (
  SELECT
    1 AS user_id,
    ARRAY_CONSTRUCT('item1', 'item2', 'item3') AS items
  UNION ALL
  SELECT
    2 AS user_id,
    ARRAY_CONSTRUCT('itemA', 'itemB') AS items
)
SELECT
  user_id,
  value AS item
FROM
  users,
  LATERAL FLATTEN(input => items) as value;

-- databricks sql:
WITH users AS (
  SELECT
    1 AS user_id,
    ARRAY('item1', 'item2', 'item3') AS items
  UNION ALL
  SELECT
    2 AS user_id,
    ARRAY('itemA', 'itemB') AS items
)
SELECT
  user_id,
  value AS item
FROM users
  LATERAL VIEW EXPLODE(items) AS value;
