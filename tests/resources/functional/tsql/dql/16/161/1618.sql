--Query type: DQL
DECLARE @h geography = ( SELECT geography::STGeomFromText('POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))', 0) FROM ( VALUES (1) ) AS t(c) ); SELECT @h.STConvexHull().ToString();
