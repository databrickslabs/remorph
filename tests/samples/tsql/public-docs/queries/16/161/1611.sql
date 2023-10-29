-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/envelopecenter-geography-data-type?view=sql-server-ver16

DECLARE @g geography = 'LINESTRING(-120 45, -120 0, -90 0)';  
SELECT @g.EnvelopeCenter().ToString();