-- see https://docs.snowflake.com/en/sql-reference/functions/strip_null_value

CREATE OR REPLACE TABLE mytable
(
  SRC Variant
);

INSERT INTO mytable
  SELECT PARSE_JSON(column1)
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
  }');

SELECT STRIP_NULL_VALUE(src:c) FROM mytable;
