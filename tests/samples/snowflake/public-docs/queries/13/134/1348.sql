-- see https://docs.snowflake.com/en/sql-reference/functions/st_centroid

SELECT ST_CENTROID(
    TO_GEOGRAPHY(
        'LINESTRING(0 0, 0 -2)'
    )
) as center_of_linestring;