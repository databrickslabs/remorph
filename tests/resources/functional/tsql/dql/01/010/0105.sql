-- tsql sql:
SELECT geography1.STIntersection(geography2).STAsText() AS intersection_of_objects
FROM (
    VALUES (
        geography::Parse('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))'),
        geography::Parse('POLYGON((3 0, 3 4, 2 4, 1 3, 2 2, 1 1, 2 0, 3 0))')
    )
) AS geography_objects(geography1, geography2);
