-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

USE WideWorldImporters;

SELECT CustomerTransactionID,
    DATETRUNC(month, TransactionDate) AS MonthTransactionOccurred,
    InvoiceID,
    CustomerID,
    TransactionAmount,
    SUM(TransactionAmount) OVER (
        PARTITION BY CustomerID ORDER BY TransactionDate,
            CustomerTransactionID ROWS UNBOUNDED PRECEDING
        ) AS RunningTotal,
    TransactionDate AS ActualTransactionDate
FROM [WideWorldImporters].[Sales].[CustomerTransactions]
WHERE InvoiceID IS NOT NULL
    AND DATETRUNC(month, TransactionDate) >= '2015-12-01';