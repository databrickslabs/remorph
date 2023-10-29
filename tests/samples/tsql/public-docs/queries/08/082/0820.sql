-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql?view=sql-server-ver16

BULK INSERT AdventureWorks2022.Sales.SalesOrderDetail
   FROM 'f:\orders\lineitem.tbl'
   WITH
     (
         FIELDTERMINATOR = ' |'
         , ROWTERMINATOR = ':\n'
         , FIRE_TRIGGERS
      );