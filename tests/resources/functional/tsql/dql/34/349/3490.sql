-- tsql sql:
WITH temp_result AS (
    SELECT 1 AS CustomerTransactionID, '2020-01-01' AS TransactionDate, 100 AS InvoiceID, 1 AS CustomerID, 100.00 AS TransactionAmount
    UNION ALL
    SELECT 2, '2020-01-15', 200, 1, 200.00
    UNION ALL
    SELECT 3, '2020-02-01', 300, 2, 300.00
)
SELECT CustomerTransactionID, DATETRUNC(month, TransactionDate) AS MonthTransactionOccurred, InvoiceID, CustomerID, TransactionAmount, SUM(TransactionAmount) OVER (
    PARTITION BY CustomerID
    ORDER BY TransactionDate, CustomerTransactionID
    ROWS UNBOUNDED PRECEDING
) AS RunningTotal, TransactionDate AS ActualTransactionDate
FROM temp_result
WHERE InvoiceID IS NOT NULL AND DATETRUNC(month, TransactionDate) >= '2020-01-01';
