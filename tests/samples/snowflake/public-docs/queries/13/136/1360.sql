-- see https://docs.snowflake.com/en/sql-reference/functions/st_dwithin

SELECT ST_DWITHIN (ST_MAKEPOINT(0, 0), ST_MAKEPOINT(1, 0), 150000);