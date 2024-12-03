--Query type: DQL
SELECT AVG(DISTINCT retail_price) AS average_retail_price
FROM (
    VALUES (10.99), (9.99), (12.99), (8.99)
) AS temp_result (retail_price);
