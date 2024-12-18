-- tsql sql:
WITH temp AS (SELECT geography::Point(10, 20, 4326).MakeValid() AS geom)
SELECT geom.STIsValid()
FROM temp;
