--Query type: DDL
SELECT SalesPerson, SalesAmount FROM (VALUES ('John', 1000), ('Jane', 2000), ('Bob', 3000)) AS SalesData (SalesPerson, SalesAmount);