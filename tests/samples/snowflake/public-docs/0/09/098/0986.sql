-- These two polygons are disjoint and do not intersect.
SELECT ST_DISJOINT(
    TO_GEOGRAPHY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))'),
    TO_GEOGRAPHY('POLYGON((3 3, 5 3, 5 5, 3 5, 3 3))')
    );