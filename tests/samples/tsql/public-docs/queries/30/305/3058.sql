-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table?view=sql-server-ver16

UPDATE [dbo].[FactResellerSalesXL_CCI] WITH (ROWLOCK)
SET UnitPrice = 50
WHERE ProductKey = 150;