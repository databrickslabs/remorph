--Query type: DDL
CREATE TABLE #temp_table
(
    _id INT IDENTITY(1, 1) PRIMARY KEY,
    account_balance VARBINARY(MAX),
    account_balance_json AS CAST(DECOMPRESS(account_balance) AS NVARCHAR(MAX))
);

WITH temp AS
(
    SELECT COMPRESS(CONVERT(VARBINARY(MAX), '1000.00')) AS account_balance
    UNION ALL
    SELECT COMPRESS(CONVERT(VARBINARY(MAX), '2000.00')) AS account_balance
)
INSERT INTO #temp_table (account_balance)
SELECT account_balance
FROM temp;

SELECT account_balance_json, _id
FROM #temp_table;
