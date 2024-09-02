--Query type: DQL
WITH geography_data AS ( SELECT geography::Point(10, 10, 4326) AS geo ) SELECT geo.InstanceOf('Point') AS is_point, geo.InstanceOf('Polygon') AS is_polygon FROM geography_data