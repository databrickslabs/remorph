--Query type: DDL
DECLARE @endpoint_name sysname = 'ipv6_endpoint_special';
DECLARE @listener_port int = 55555;
DECLARE @listener_ip nvarchar(50) = '::1';

EXEC sp_create_endpoint @endpoint_name, @listener_port, @listener_ip;

SELECT * FROM sys.endpoints WHERE name = @endpoint_name;

-- REMORPH CLEANUP: DROP ENDPOINT ipv6_endpoint_special;