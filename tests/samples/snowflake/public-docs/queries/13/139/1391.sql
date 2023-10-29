-- see https://docs.snowflake.com/en/sql-reference/functions/st_srid

SELECT ST_SRID(ST_MAKEPOINT(37.5, 45.5));