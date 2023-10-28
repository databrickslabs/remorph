SELECT ST_DISTANCE(
         ST_GEOM_POINT(13.4814, 52.5015),
         ST_GEOM_POINT(-121.8212, 36.8252))
       AS distance_in_degrees;