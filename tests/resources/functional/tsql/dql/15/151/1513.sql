-- tsql sql:
DECLARE @angle float;
SET @angle = 14.78;
WITH angle AS (
    SELECT @angle AS angle_value
)
SELECT 'The COS of the angle is: ' + CONVERT(VARCHAR, COS(angle_value)) AS result
FROM angle;
