--Query type: DDL
WITH temp_result AS (
    SELECT *
    FROM (
        VALUES
            (1, 1000000),
            (2, 2000000),
            (3, 3000000)
    ) AS temp_result(TransactionID, totalprice)
)
SELECT *
FROM temp_result;
