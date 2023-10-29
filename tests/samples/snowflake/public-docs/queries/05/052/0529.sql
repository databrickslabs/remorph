-- see https://docs.snowflake.com/en/sql-reference/functions-analytic

CREATE TABLE t (x INT, y INT);
INSERT INTO t (x, y) VALUES
  (1, 2),         -- No NULLs.
  (3, NULL),      -- One but not all columns are NULL.
  (NULL, 6),      -- One but not all columns are NULL.
  (NULL, NULL);   -- All columns are NULL.