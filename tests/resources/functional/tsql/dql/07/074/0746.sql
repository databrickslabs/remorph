--Query type: DQL
WITH geography_data AS (
  SELECT geography::Point(10, 20, 4326) AS g
  UNION ALL
  SELECT geography::Point(30, 40, 4326) AS g
  UNION ALL
  SELECT geography::Point(50, 60, 4326) AS g
)
SELECT
  g,
  g.Long AS ST_X_g,
  g.Lat AS ST_Y_g
FROM geography_data
ORDER BY g.Long;
