-- see https://docs.snowflake.com/en/sql-reference/functions-regexp

SELECT w2, REGEXP_REPLACE(w2, '(.old)', $$very \1$$)
  FROM wildcards
  ORDER BY w2;