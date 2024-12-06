-- tsql sql:
SELECT *
INTO #customer_mv
FROM (
    VALUES (1, 'John', 'Doe'),
           (2, 'Jane', 'Doe')
) AS customer (c_custkey, c_name, c_address);

EXEC sp_rename '#customer_mv', '#my_customer_mv';

SELECT *
FROM #my_customer_mv;

-- REMORPH CLEANUP: DROP TABLE #my_customer_mv;
