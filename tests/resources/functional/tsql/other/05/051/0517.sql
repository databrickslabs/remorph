--Query type: DCL
WITH temp_result AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, 'Address1', 'Phone1', 'Comment1', 1),
            (2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2', 2)
    ) AS temp_table (
        custkey,
        name,
        acctbal,
        address,
        phone,
        comment,
        nationkey
    )
)
SELECT *
FROM temp_result;
