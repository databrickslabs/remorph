-- see https://learn.microsoft.com/en-us/sql/t-sql/lesson-1-creating-database-objects?view=sql-server-ver16

CREATE VIEW vw_Names
   AS
   SELECT ProductName, Price FROM Products;
GO