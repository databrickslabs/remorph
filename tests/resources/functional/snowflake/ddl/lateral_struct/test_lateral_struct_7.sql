-- snowflake sql:
SELECT
  v,
  v:food AS food,
  TO_JSON(v) AS v_as_json
FROM (
  SELECT PARSE_JSON('{"food": "apple"}') AS v
) t;

-- databricks sql:
SELECT
  v,
  v:food AS food,
  TO_JSON(v) AS v_as_json
FROM (
  SELECT
    PARSE_JSON('{"food": "apple"}') AS v
) AS t;
