--Query type: DDL
CREATE FUNCTION myFunction()
RETURNS TABLE
AS
RETURN
    SELECT BusinessEntityID, TotalDue
    FROM (
        VALUES (1, 100.0), (2, 200.0), (3, 300.0)
    ) AS temp_result (BusinessEntityID, TotalDue)
    WHERE BusinessEntityID = 1;
