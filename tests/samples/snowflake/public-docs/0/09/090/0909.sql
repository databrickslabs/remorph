SELECT TO_GEOGRAPHY('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))') AS polygon,
       TO_GEOGRAPHY('POINT(0 2)') AS point,
       ST_DWITHIN(polygon, point, 0) AS point_is_on_top_of_polygon,
       ST_INTERSECTION(polygon, point);