SELECT ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.306100 37.554162)'),
    5) AS less_precise_geohash_a;