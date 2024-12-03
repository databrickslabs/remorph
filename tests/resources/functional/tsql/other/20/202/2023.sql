--Query type: DDL
DECLARE @service_id INT;

WITH service_id_cte AS (
    SELECT service_id
    FROM sys.services
    WHERE name = '//TPC-H.com/Orders'
)

SELECT @service_id = service_id
FROM service_id_cte;

IF @service_id IS NOT NULL
BEGIN
    DECLARE @sql NVARCHAR(MAX) = 'DROP SERVICE ' + CONVERT(NVARCHAR(MAX), @service_id);
    EXEC sp_executesql @sql;
    PRINT 'Service dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Service not found.';
END
