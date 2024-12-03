--Query type: TCL
CREATE PROCEDURE usp_GetCustomerErrorInfo
    @customerkey INT
AS
BEGIN TRY
    SELECT c_name, o_totalprice / 0 AS error_column
    FROM (
        VALUES (1, 'Customer1', 1, 100.0),
               (2, 'Customer2', 2, 200.0)
    ) AS c (c_customerkey, c_name, o_orderkey, o_totalprice)
    WHERE c_customerkey = @customerkey;
END TRY
BEGIN CATCH
    SELECT 'Error handling completed' AS status;
END CATCH;
EXEC usp_GetCustomerErrorInfo @customerkey = 1;
SELECT *
FROM (
    VALUES (1, 'Customer1', 1, 100.0),
           (2, 'Customer2', 2, 200.0)
) AS c (c_customerkey, c_name, o_orderkey, o_totalprice);
-- REMORPH CLEANUP: DROP PROCEDURE usp_GetCustomerErrorInfo;
