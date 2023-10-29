-- see https://docs.snowflake.com/en/sql-reference/functions/median

SELECT k, MEDIAN(v) FROM aggr GROUP BY k ORDER BY k;