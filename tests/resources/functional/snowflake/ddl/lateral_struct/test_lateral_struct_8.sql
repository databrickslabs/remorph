-- snowflake sql:
SELECT PARSE_JSON(src.col):c AS c
FROM VALUES
  ('{"a": "1", "b": "2", "c": null}'),
  ('{"a": "1", "b": "2", "c": "3"}') AS src(col);

-- databricks sql:
SELECT
  FROM_JSON(src.col, schema_of_json('{SRC.COL_SCHEMA}')).c AS c
FROM VALUES
   ('{"a": "1", "b": "2", "c": null}'),
   ('{"a": "1", "b": "2", "c": "3"}') AS src(col);

-- experimental sql:
SELECT
  PARSE_JSON(src.col).c AS c
FROM VALUES
   ('{"a": "1", "b": "2", "c": null}'),
   ('{"a": "1", "b": "2", "c": "3"}') AS src(col);