-- tsql sql:
SELECT nation, geography::UnionAggregate(region_geo) AS region_geo FROM (VALUES ('USA', geography::Point(40.7128, -74.0060, 4326)), ('Canada', geography::Point(51.5074, -0.1278, 4326))) AS region(nation, region_geo) WHERE nation LIKE 'U%' GROUP BY nation;
