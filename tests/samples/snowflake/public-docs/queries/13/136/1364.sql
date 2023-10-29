-- see https://docs.snowflake.com/en/sql-reference/functions/st_envelope

SELECT ST_ENVELOPE(
    TO_GEOGRAPHY(
        'POLYGON((-122.306067 37.55412, -122.32328 37.561801, -122.325879 37.586852, -122.306067 37.55412))'
    )
) as minimum_bounding_box_around_polygon;