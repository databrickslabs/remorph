-- tsql sql:
WITH temp_result AS (
    SELECT p_name, p_retailprice
    FROM (
        VALUES ('Product1', 10.99),
               ('Product2', 9.99),
               ('Product3', 12.99)
    ) AS products (p_name, p_retailprice)
)
SELECT p_name, p_retailprice, FIRST_VALUE(p_name) OVER (ORDER BY p_retailprice ASC) AS LeastExpensive
FROM temp_result
WHERE p_retailprice > 9.99;
