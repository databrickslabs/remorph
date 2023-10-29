-- see https://docs.snowflake.com/en/sql-reference/data-types-geospatial

SELECT TO_GEOMETRY(ST_ASGEOJSON(geography_expression), 4326);