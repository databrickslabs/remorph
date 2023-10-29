-- see https://docs.snowflake.com/en/sql-reference/sql/insert-multi-table

-- Returns error
  INSERT ALL
    WHEN c > 10 THEN
      INTO t1 (col1, col2) VALUES (a, b)
  SELECT a FROM src;

-- Completes successfully
  INSERT ALL
    WHEN c > 10 THEN
      INTO t1 (col1, col2) VALUES (a, b)
  SELECT a, b, c FROM src;