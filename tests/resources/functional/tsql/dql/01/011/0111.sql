--Query type: DQL
SELECT geography::STGeomFromText(geo_string, 4326).STStartPoint() AS start_point
FROM (
    VALUES ('LINESTRING(10 10, 20 20, 30 30, 40 40)')
) AS geography_data(geo_string);