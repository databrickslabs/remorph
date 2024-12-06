-- tsql sql:
WITH geography_values AS (
  SELECT id, geography::Parse('POLYGON((0 0, 1 0, 2 1, 1 2, 2 3, 1 4, 0 4, 0 0))') AS geography
  FROM (VALUES (1)) AS v(id)
  UNION ALL
  SELECT id, geography::Parse('POLYGON((3 0, 3 4, 2 4, 1 3, 2 2, 1 1, 2 0, 3 0))') AS geography
  FROM (VALUES (2)) AS v(id)
)
SELECT gv1.geography.STSymDifference(gv2.geography) AS symmetric_difference_between_objects
FROM geography_values AS gv1
CROSS JOIN geography_values AS gv2
WHERE gv1.id != gv2.id;
