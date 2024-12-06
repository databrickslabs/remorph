-- tsql sql:
DECLARE @Region nvarchar(50), @TotalRevenue DECIMAL(10, 2);
SET @Region = N'ASIA';
SET @TotalRevenue = 1000000.00;

SELECT c.c_name, c.c_address, o.o_totalprice
FROM (
    VALUES (
        1, 'Customer1', 'Address1', 'ASIA'),
        (2, 'Customer2', 'Address2', 'EUROPE'),
        (3, 'Customer3', 'Address3', 'ASIA')
    ) AS c (c_custkey, c_name, c_address, c_region)
JOIN (
    VALUES (
        1, 1, 1000.00),
        (2, 1, 2000.00),
        (3, 2, 500.00),
        (4, 3, 1500.00)
    ) AS o (o_orderkey, o_custkey, o_totalprice)
ON c.c_custkey = o.o_custkey
WHERE c.c_region = @Region AND o.o_totalprice >= @TotalRevenue;
