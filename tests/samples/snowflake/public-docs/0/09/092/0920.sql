SELECT ST_ENVELOPE(
    TO_GEOGRAPHY(
        'POINT(-122.32328 37.561801)'
    )
) as minimum_bounding_box_around_point;