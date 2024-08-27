-- snowflake sql:
SELECT v, v:food, TO_JSON(v) FROM jdemo1;

--revised snowflake sql
SELECT
  v,
  v:food AS food,
  to_json(v) AS v_as_json
FROM (
  SELECT OBJECT_CONSTRUCT('food', 'apple') AS v
) t;

-- databricks sql:
SELECT v, v.food, TO_JSON(v) FROM jdemo1;

--revised databricks sql
SELECT
  v,
  v.food,
  TO_JSON(v)
FROM (
  SELECT STRUCT('apple' AS food) AS v
) t;
