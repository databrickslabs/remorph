-- snowflake sql:
WITH users AS (
  SELECT
    1 AS user_id,
    '[{"id":1,"name":"A"},{"id":2,"name":"B"}]' AS json_data
  UNION ALL
  SELECT
    2 AS user_id,
    '[{"id":3,"name":"C"},{"id":4,"name":"D"}]' AS json_data
)
SELECT
  user_id,
  value AS json_item
FROM
  users,
  LATERAL FLATTEN(input => PARSE_JSON(json_data)) as value;

-- databricks sql:
WITH users AS (
  SELECT
    1 AS user_id,
    '[{"id":1,"name":"A"},{"id":2,"name":"B"}]' AS json_data
  UNION ALL
  SELECT
    2 AS user_id,
    '[{"id":3,"name":"C"},{"id":4,"name":"D"}]' AS json_data
)
SELECT
  user_id,
  value AS json_item
FROM
  users ,
  LATERAL VARIANT_EXPLODE(PARSE_JSON(json_data)) AS value
