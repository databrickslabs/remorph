-- see https://docs.snowflake.com/en/sql-reference/functions/row_number

SELECT state, bushels_produced, ROW_NUMBER()
  OVER (ORDER BY bushels_produced DESC)
  FROM corn_production;
