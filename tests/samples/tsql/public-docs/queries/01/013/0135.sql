-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geometry/convexhullaggregate-geometry-data-type?view=sql-server-ver16

-- Setup table variable for ConvexHullAggregate example  
DECLARE @Geom TABLE  
(  
shape geometry,  
shapeType nvarchar(50)  
)  
INSERT INTO @Geom(shape,shapeType) VALUES('CURVEPOLYGON(CIRCULARSTRING(2 3, 4 1, 6 3, 4 5, 2 3))', 'Circle'),  
('POLYGON((1 1, 4 1, 4 5, 1 5, 1 1))', 'Rectangle');  
-- Perform ConvexHullAggregate on @Geom.shape column  
SELECT geometry::ConvexHullAggregate(shape).ToString()  
FROM @Geom;