-- tsql sql:
DECLARE @h geography;
SET @h = geography::Point(24, 24, 24);
WITH temp AS (
    SELECT @h.STSrid AS result
)
SELECT * FROM temp;
