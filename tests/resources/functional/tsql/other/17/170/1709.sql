--Query type: DML
WITH g AS (SELECT geometry::Parse('MULTIPOINT((2 2),(2 5))') AS geom)
SELECT g.geom.BufferWithCurves(2).ToString() AS Buffer4,
       g.geom.BufferWithCurves(2.5).ToString() AS Buffer5,
       g.geom.BufferWithCurves(2.6).ToString() AS Buffer6
FROM g;
