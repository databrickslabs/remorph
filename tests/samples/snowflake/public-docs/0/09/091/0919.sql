SELECT ST_ENVELOPE(
    TO_GEOGRAPHY(
        'LINESTRING(-122.32328 37.561801,-122.32351 37.561801)'
    )
) as minimum_bounding_box_around_arc_along_parallel;