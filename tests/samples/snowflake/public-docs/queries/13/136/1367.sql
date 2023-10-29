-- see https://docs.snowflake.com/en/sql-reference/functions/st_geogpointfromgeohash

SELECT ST_GEOGPOINTFROMGEOHASH('9q9j8ue2v71y5zzy0s4q')
    AS geography_center_point_of_geohash;