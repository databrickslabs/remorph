--Query type: DQL
WITH geography_data AS (
    SELECT 'POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))' AS geo1,
           'POLYGON((3 3, 5 3, 5 5, 3 5, 3 3))' AS geo2
)
SELECT GEOGRAPHY::STGeomFromText(geo1, 4326).STDisjoint(GEOGRAPHY::STGeomFromText(geo2, 4326))
FROM geography_data
