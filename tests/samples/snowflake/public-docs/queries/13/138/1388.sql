-- see https://docs.snowflake.com/en/sql-reference/data-types-geospatial

SELECT ST_SETSRID(geometry_expression, 4326);