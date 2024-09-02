--Query type: DCL
DECLARE @custid INT;
SET @custid = (
    SELECT c_custkey
    FROM (
        VALUES (1, 'Customer#000000001'),
               (2, 'Customer#000000002')
    ) AS Customer (c_custkey, c_name)
);
DBCC CHECKTABLE ('(
    SELECT *
    FROM (
        VALUES (1, 10.0),
               (2, 20.0)
    ) AS Orders (o_orderkey, o_totalprice)
)', @custid);
