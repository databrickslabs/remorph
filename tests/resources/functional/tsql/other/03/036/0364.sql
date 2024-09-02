--Query type: DDL
CREATE PROCEDURE usp_CalculateArea
    @radius decimal(10, 2)
AS
BEGIN
    WITH area AS (
        SELECT 3.14 * POWER(@radius, 2) AS Area
    )
    SELECT *
    FROM area
END;