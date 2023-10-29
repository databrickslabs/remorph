-- see https://docs.snowflake.com/en/sql-reference/functions/st_geohash

SELECT ST_GEOHASH(
    TO_GEOGRAPHY('POINT(-122.306100 37.554162)'))
    AS geohash_of_point_a;