-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-symmetric-key-transact-sql?view=sql-server-ver16

CREATE SYMMETRIC KEY JanainaKey09
WITH ALGORITHM = AES_256
ENCRYPTION BY CERTIFICATE Shipping04;
GO