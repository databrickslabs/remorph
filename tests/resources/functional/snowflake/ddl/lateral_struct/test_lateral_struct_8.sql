-- snowflake sql:
SELECT STRIP_NULL_VALUE(src:c) FROM mytable;

--revised snowflake sql
SELECT STRIP_NULL_VALUE(PARSE_JSON(src.col):c)
FROM VALUES
  ('{
  "a": "1",
  "b": "2",
  "c": null
  }')
  , ('{
  "a": "1",
  "b": "2",
  "c": "3"
  }') AS src(col);

-- databricks sql:
SELECT STRIP_NULL_VALUE(src.c) FROM mytable;

-- revised databricks sql
SELECT
  CASE
    WHEN map_value['c'] IS NULL THEN NULL
    ELSE map_value['c']
  END AS c
FROM VALUES
  (MAP('a', '1', 'b', '2', 'c', NULL)),
  (MAP('a', '1', 'b', '2', 'c', '3'))
  AS src(map_value);