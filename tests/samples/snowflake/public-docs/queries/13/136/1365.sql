-- see https://docs.snowflake.com/en/sql-reference/functions/st_geogfromgeohash

SELECT ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
    AS geography_from_geohash,
    ST_AREA(ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q'))
    AS area_of_geohash;