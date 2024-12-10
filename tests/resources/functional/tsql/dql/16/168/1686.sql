-- tsql sql:
DECLARE @h geography = 'LINESTRING(-74.006 40.712, -74.005 40.711, -74.005 40.713, -74.006 40.713, -74.006 40.712)';
SELECT buffer_string
FROM (
    SELECT @h.BufferWithCurves(1).ToString() AS buffer_string
) AS cte;
