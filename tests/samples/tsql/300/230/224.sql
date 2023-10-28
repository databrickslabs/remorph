BULK INSERT AdventureWorks2022.Sales.SalesOrderDetail
   FROM 'f:\orders\lineitem.tbl'
   WITH
      (
         FIELDTERMINATOR = ' |'
         , ROWTERMINATOR = ' |\n'
      );