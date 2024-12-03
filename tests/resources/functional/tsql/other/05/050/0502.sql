--Query type: DDL
DECLARE @file_path nvarchar(255) = 'c:\SecurityProvider\SecurityProvider_v2.dll';
DECLARE @sql nvarchar(max) = N'CREATE CRYPTOGRAPHIC PROVIDER SecurityProvider FROM FILE = ''' + @file_path + ''';
SELECT * FROM sys.cryptographic_providers WHERE name = ''SecurityProvider'';';
EXEC sp_executesql @sql;
SELECT * FROM sys.cryptographic_providers WHERE name = 'SecurityProvider';
-- REMORPH CLEANUP: DROP CRYPTOGRAPHIC PROVIDER SecurityProvider;
