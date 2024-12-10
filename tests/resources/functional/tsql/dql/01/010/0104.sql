-- tsql sql:
WITH geography_data AS (
    SELECT geography::STGeomFromText('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))', 0) AS geo1,
           geography::STGeomFromText('POLYGON((3 0, 3 4, 2 4, 1 3, 2 2, 1 1, 2 0, 3 0))', 0) AS geo2
)
SELECT geo1.STDifference(geo2) AS difference_between_objects
FROM geography_data;
