-- see https://docs.snowflake.com/en/sql-reference/functions/st_geohash

SELECT
    ST_GEOHASH(
        TO_GEOGRAPHY(
            'POLYGON((-122.306100 37.554162, -122.306100 37.562333, -122.323111 37.562333, -122.323111 37.554162, -122.306100 37.554162))'
        )
    ) AS geohash_of_polygon;