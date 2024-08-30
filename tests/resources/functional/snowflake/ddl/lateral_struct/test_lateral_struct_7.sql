-- snowflake sql:
SELECT
  v,
  v:food AS food,
  to_json(v) AS v_as_json
FROM (
  SELECT OBJECT_CONSTRUCT('food', 'apple') AS v
) t;

-- databricks sql:
SELECT
  v,
  v.food AS food,
  TO_JSON(v) AS v_as_json
FROM (
  SELECT STRUCT('apple' AS food) AS v
) AS t;
