-- tsql sql:
WITH OrdersCTE AS (
    SELECT
        O_ORDERKEY = 1,
        O_CUSTKEY = 1,
        O_ORDERSTATUS = 'A',
        O_TOTALPRICE = 100.00,
        O_ORDERDATE = '2022-01-01',
        O_ORDERPRIORITY = 'High',
        O_CLERK = 'John',
        O_SHIPPRIORITY = 1,
        O_COMMENT = 'Sample comment'
)
SELECT *
FROM OrdersCTE;
