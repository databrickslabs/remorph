SELECT ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6)
    AS geography_from_less_precise_geohash,
    ST_AREA(ST_GEOGFROMGEOHASH('9q9j8ue2v71y5zzy0s4q', 6))
    AS area_of_geohash;