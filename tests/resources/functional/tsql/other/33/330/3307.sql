--Query type: DDL
WITH customer AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1', 100.00, '123 Main St', '123-456-7890', 'Comment1', 1),
            (2, 'Customer2', 200.00, '456 Elm St', '987-654-3210', 'Comment2', 2)
    ) AS c (custkey, name, acctbal, address, phone, comment, nationkey)
)
SELECT
    c.custkey,
    c.name,
    c.acctbal,
    c.address,
    c.phone,
    c.comment
FROM
    customer c
WHERE
    c.acctbal > 0.00
ORDER BY
    c.acctbal DESC;