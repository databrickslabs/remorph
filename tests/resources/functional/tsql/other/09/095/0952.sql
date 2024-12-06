-- tsql sql:
DECLARE @sql nvarchar(max) = N'CREATE ENDPOINT endpoint_replication STATE = STARTED AS TCP ( LISTENER_PORT = 7033 ) FOR DATABASE_MIRRORING ( AUTHENTICATION = WINDOWS KERBEROS, ENCRYPTION = SUPPORTED, ROLE=ALL);';
DECLARE @params nvarchar(max) = N'@listener_port int, @authentication nvarchar(50), @encryption nvarchar(50), @role nvarchar(50)';
DECLARE @listener_port int = 7033;
DECLARE @authentication nvarchar(50) = 'WINDOWS KERBEROS';
DECLARE @encryption nvarchar(50) = 'SUPPORTED';
DECLARE @role nvarchar(50) = 'ALL';

WITH temp_result_set AS (
    SELECT @listener_port AS listener_port, @authentication AS authentication, @encryption AS encryption, @role AS role
)
SELECT @sql = REPLACE(@sql, 'LISTENER_PORT = 7033', 'LISTENER_PORT = ' + CONVERT(nvarchar(10), listener_port))
FROM temp_result_set;

EXEC sp_executesql @sql, @params, @listener_port = @listener_port, @authentication = @authentication, @encryption = @encryption, @role = @role;
