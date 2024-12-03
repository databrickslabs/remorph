--Query type: DCL
DECLARE @sql nvarchar(max);
DECLARE @CredentialName nvarchar(50) = 'NewSaddle';
DECLARE @IdentityValue nvarchar(50) = 'RettigB';
DECLARE @SecretValue nvarchar(50) = 'sdrlk8$40-dksli87nNN8';

SET @sql = 'ALTER CREDENTIAL ' + QUOTENAME(@CredentialName) + ' WITH IDENTITY = ''' + @IdentityValue + ''', SECRET = ''' + @SecretValue + '''';

EXEC sp_executesql @sql;

-- To verify the creation of the credential, you can use the following query:
SELECT * FROM sys.credentials WHERE name = @CredentialName;

-- REMORPH CLEANUP: DROP CREDENTIAL [NewSaddle];
