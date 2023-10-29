-- see https://docs.snowflake.com/en/sql-reference/functions/st_srid

SELECT ST_SRID(ST_MAKEPOINT(NULL, NULL)), ST_SRID(NULL);