-- see https://docs.snowflake.com/en/sql-reference/functions/st_hausdorffdistance

SELECT ST_HAUSDORFFDISTANCE(ST_POINT(0, 0), ST_POINT(0, 1));