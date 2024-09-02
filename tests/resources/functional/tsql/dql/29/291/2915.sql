--Query type: DQL
WITH customer_data AS (
    SELECT c_name, c_custkey, SUBSTRING(c_name, 1, 1) AS Initial,
           SUBSTRING(c_name, 3, 2) AS ThirdAndFourthCharacters
    FROM (
        VALUES ('Customer#000000001', 1),
               ('Customer#000000002', 2),
               ('Customer#000000003', 3),
               ('Customer#000000004', 4)
    ) AS customers (c_name, c_custkey)
)
SELECT c_name, Initial, ThirdAndFourthCharacters
FROM customer_data
WHERE c_custkey < 5;