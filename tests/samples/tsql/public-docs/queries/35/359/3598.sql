-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/unary-operators-negative?view=sql-server-ver16

USE ssawPDW;  
  
SELECT TOP (1) - ( - 17) FROM DimEmployee;