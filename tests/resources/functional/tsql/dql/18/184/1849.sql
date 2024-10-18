--Query type: DQL
DECLARE @geo bit;
WITH geography_data AS (
    SELECT geography::Point(1, 1, 1) AS geo
)
SELECT @geo = geo.HasZ
FROM geography_data;
SELECT @geo AS result;