-- tsql sql:
WITH region AS ( SELECT -71.0882 AS lon1, 42.3152 AS lat1, -71.0882 AS lon2, 42.3263 AS lat2, -71.1022 AS lon3, 42.3263 AS lat3, -71.1022 AS lon4, 42.3152 AS lat4 ) SELECT lon1, lat1, lon2, lat2, lon3, lat3, lon4, lat4 FROM region;
