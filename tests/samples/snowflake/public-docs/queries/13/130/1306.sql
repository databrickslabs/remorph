-- see https://docs.snowflake.com/en/sql-reference/functions/round

SELECT ROUND(
  EXPR => -2.5,
  SCALE => 0,
  ROUNDING_MODE => 'HALF_TO_EVEN');