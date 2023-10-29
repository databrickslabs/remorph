-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

DELETE Sales.ShoppingCartItem
    OUTPUT DELETED.*;