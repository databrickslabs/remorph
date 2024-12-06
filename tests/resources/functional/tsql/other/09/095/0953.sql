-- tsql sql:
DECLARE @endpoint_name sysname = 'ipv4_endpoint_special';
DECLARE @grantee sysname = 'public';
DECLARE @sql nvarchar(max);

-- Create the endpoint
SET @sql = N'CREATE ENDPOINT ' + QUOTENAME(@endpoint_name) + N'
STATE = STARTED
AS TCP (LISTENER_PORT = 55555, LISTENER_IP = (10.0.75.1))
FOR TSQL ()';
EXEC sp_executesql @sql;

-- Grant connect permission
SET @sql = N'GRANT CONNECT ON ENDPOINT::' + QUOTENAME(@endpoint_name) + N' TO ' + QUOTENAME(@grantee);
EXEC sp_executesql @sql;

-- Select statement to show the data
SELECT * FROM sys.endpoints WHERE name = @endpoint_name;

-- REMORPH CLEANUP: DROP ENDPOINT ipv4_endpoint_special;
