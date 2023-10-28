WITH
    a AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 1, 1 0, 0 -1, -1 0))')),
    b AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 1, 2 0, 0 -1, -1 0))')),
    c AS (TO_GEOGRAPHY('POLYGON((-1 0, 0 3, 1 0, 0 -1, -1 0))'))
SELECT
    ST_HAUSDORFFDISTANCE(a, b) as distance_between_a_and_b,
    ST_HAUSDORFFDISTANCE(a, c) as distance_between_a_and_c;