-- see https://docs.snowflake.com/en/sql-reference/functions/coalesce

SELECT column1, column2, column3, coalesce(column1, column2, column3)
FROM (values
  (1,    2,    3   ),
  (null, 2,    3   ),
  (null, null, 3   ),
  (null, null, null),
  (1,    null, 3   ),
  (1,    null, null),
  (1,    2,    null)
) v;
