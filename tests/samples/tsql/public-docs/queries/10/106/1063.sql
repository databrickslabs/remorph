-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16

CREATE NONCLUSTERED INDEX IX_TransactionHistory_ReferenceOrderID
  ON Production.TransactionHistory (ReferenceOrderID)
  ON TransactionsPS1 (TransactionDate);
GO