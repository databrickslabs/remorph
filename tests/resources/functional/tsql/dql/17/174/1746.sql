-- tsql sql:
WITH geography_data AS ( SELECT geography::Point(10, 20, 4326) AS geo ) SELECT geo.STAsText() AS geo_text FROM geography_data;
