-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-columnstore-index-transact-sql?view=sql-server-ver16

CREATE CLUSTERED COLUMNSTORE INDEX [OrderedCCI] ON dbo.FactResellerSalesPartCategoryFull
ORDER (EnglishProductSubcategoryName, EnglishProductName)
WITH (MAXDOP = 1, DROP_EXISTING = ON);