-- tsql sql:
WITH geography_data AS ( SELECT geography::STGeomFromText('LINESTRING(1 1, 2 2, 3 3, 4 4)', 0) AS geography_string ) SELECT geography_string.STPointN(2) FROM geography_data;
