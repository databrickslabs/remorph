-- see https://docs.snowflake.com/en/sql-reference/functions/dateadd

SELECT TO_TIMESTAMP_LTZ('2013-05-08 11:22:33.444') AS v1,
  DATEADD(HOUR, 2, TO_TIMESTAMP_LTZ('2013-05-08 11:22:33.444')) AS v;