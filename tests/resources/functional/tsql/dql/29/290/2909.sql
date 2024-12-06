-- tsql sql:
WITH customer_info AS (
    SELECT c_name, c_password
    FROM (
        VALUES ('Customer#000000001', 'password123'),
               ('Customer#000000002', 'password456')
    ) AS customer (c_name, c_password)
)
SELECT c_name
FROM customer_info
WHERE PWDCOMPARE('', c_password) = 1;
