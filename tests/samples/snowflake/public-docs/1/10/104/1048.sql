SELECT
    ST_GEOHASH(
        TO_GEOGRAPHY('POINT(-122.306100 37.554162)'))
        AS geohash_of_point_a,
    ST_GEOHASH(
        TO_GEOGRAPHY('POINT(-122.323111 37.562333)'))
        AS geohash_of_point_b;
SELECT
    ST_GEOHASH(
        TO_GEOGRAPHY('POINT(-122.306100 37.554162)'),
        5) AS less_precise_geohash_a,
    ST_GEOHASH(
        TO_GEOGRAPHY('POINT(-122.323111 37.562333)'),
        5) AS less_precise_geohash_b;