--Query type: DQL
DECLARE @mymoney DECIMAL(10, 2) = 3148.29;
WITH mymoney AS (
    SELECT CAST(@mymoney AS DECIMAL(10,2)) AS value
)
SELECT CAST(value AS DECIMAL) AS money_decimal, CAST(value AS VARCHAR(20)) AS money_varchar
FROM mymoney;