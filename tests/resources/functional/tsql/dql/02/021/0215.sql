-- tsql sql:
DECLARE @sql NVARCHAR(MAX) = 'EXEC tpch_sf1.customer_GET_CUSTOMER_INFO';
DECLARE @customer_info TABLE (
    customer_info NVARCHAR(MAX)
);
INSERT INTO @customer_info
EXEC sp_executesql @sql;
SELECT *
FROM @customer_info;
