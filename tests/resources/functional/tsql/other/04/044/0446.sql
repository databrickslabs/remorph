--Query type: DCL
DECLARE @customerName NVARCHAR(32) = 'John Smith';
SELECT *
FROM (
    VALUES (@customerName)
) AS CustomerNameTable (
    CustomerName
);