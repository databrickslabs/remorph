--Query type: DQL
WITH temp_result AS (SELECT TOP (1) 3 % 2 AS calc FROM (VALUES (1)) AS t (c)) SELECT * FROM temp_result;