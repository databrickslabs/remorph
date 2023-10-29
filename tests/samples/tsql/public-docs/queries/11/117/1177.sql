-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-symmetric-key-transact-sql?view=sql-server-ver16

CREATE SYMMETRIC KEY MySymKey
AUTHORIZATION User1
FROM PROVIDER EKMProvider
WITH
PROVIDER_KEY_NAME='KeyForSensitiveData',
CREATION_DISPOSITION=OPEN_EXISTING;
GO