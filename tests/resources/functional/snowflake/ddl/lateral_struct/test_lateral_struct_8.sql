-- snowflake sql:
SELECT PARSE_JSON(src.col):i AS i
FROM VALUES
  ('{"a": "1", "b": "2", "i": null}'),
  ('{"a": "1", "b": "2", "i": "3"}') AS src(col);

-- databricks sql:
SELECT
  PARSE_JSON(src.col):i AS i
FROM VALUES
  ('{"a": "1", "b": "2", "i": null}'),
  ('{"a": "1", "b": "2", "i": "3"}') AS src(col);
