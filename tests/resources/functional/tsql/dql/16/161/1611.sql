-- tsql sql:
DECLARE @region geography = 'LINESTRING(-100 40, -100 -5, -80 -5)';
WITH temp_result AS (
  SELECT @region.EnvelopeCenter() AS center
)
SELECT center.ToString() AS region_center
FROM temp_result;
