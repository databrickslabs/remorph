-- snowflake sql:
SELECT PARSE_JSON(src.col):c AS c
FROM VALUES
  ('{"a": "1", "b": "2", "c": null}'),
  ('{"a": "1", "b": "2", "c": "3"}') AS src(col);

-- databricks sql:
SELECT
  PARSE_JSON(src.col):c AS c
FROM VALUES
  ('{"a": "1", "b": "2", "c": null}'),
  ('{"a": "1", "b": "2", "c": "3"}') AS src(col);
