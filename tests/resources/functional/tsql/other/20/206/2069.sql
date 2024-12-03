--Query type: DCL
DECLARE @server_name sysname, @server_type sysname;

DECLARE cur_servers CURSOR FOR
    SELECT server_name, server_type
    FROM (
        VALUES ('linked_server_name', 'SQL Server')
    ) AS servers (server_name, server_type);

OPEN cur_servers;

FETCH NEXT FROM cur_servers INTO @server_name, @server_type;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC sp_addlinkedserver @server_name, @server_type;

    FETCH NEXT FROM cur_servers INTO @server_name, @server_type;
END

CLOSE cur_servers;

DEALLOCATE cur_servers;
