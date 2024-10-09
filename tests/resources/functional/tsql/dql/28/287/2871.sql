--Query type: DQL
WITH customer AS (
    SELECT 'Customer#000000001' AS c_name, 'United States' AS c_nationkey
),

nation AS (
    SELECT 'United States' AS n_name, 1 AS n_nationkey
)

SELECT 
    c.c_name AS customer_name,
    'UPDATE CUSTOMER SET c_nationkey = ' + CONVERT(VARCHAR(10), n.n_nationkey) + ' WHERE c_name = ''Customer#000000001''' AS update_command
FROM 
    customer c
    JOIN nation n ON c.c_nationkey = n.n_nationkey
WHERE 
    n.n_name = 'United States'