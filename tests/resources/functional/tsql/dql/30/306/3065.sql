--Query type: DQL
SELECT nation, geography::EnvelopeAggregate(location) AS location FROM (VALUES ('USA', geography::Point(47.65100, -122.34900, 4326)), ('Canada', geography::Point(49.89510, -97.13840, 4326))) AS region(nation, location) WHERE nation LIKE 'USA%' GROUP BY nation
