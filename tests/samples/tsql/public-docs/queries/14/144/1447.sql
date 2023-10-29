-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/binary-and-varbinary-transact-sql?view=sql-server-ver16

DECLARE @BinaryVariable2 BINARY(2);
  
SET @BinaryVariable2 = 123456;
SET @BinaryVariable2 = @BinaryVariable2 + 1;
  
SELECT CAST( @BinaryVariable2 AS INT);
GO