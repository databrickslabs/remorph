-- tsql sql:
DECLARE @orderdateoffset datetimeoffset(4) = '1995-03-01 12:00:00.0000 +00:00';
DECLARE @orderdate datetime = CAST(@orderdateoffset AS datetime);

WITH cte AS (
    SELECT @orderdateoffset AS 'orderdateoffset', @orderdate AS 'orderdate'
)
SELECT * FROM cte;
