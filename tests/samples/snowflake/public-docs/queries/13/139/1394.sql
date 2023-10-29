-- see https://docs.snowflake.com/en/sql-reference/data-types-geospatial

SELECT ST_TRANSFORM(geometry_expression, 4326, 28992);