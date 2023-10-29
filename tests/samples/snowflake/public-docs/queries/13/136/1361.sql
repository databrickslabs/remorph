-- see https://docs.snowflake.com/en/sql-reference/functions/st_envelope

SELECT ST_ENVELOPE(
    TO_GEOGRAPHY(
        'LINESTRING(-122.32328 37.561801, -122.32328 37.562001)'
    )
) as minimum_bounding_box_around_meridian_arc;