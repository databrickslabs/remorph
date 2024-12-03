--Query type: DQL
SELECT server_name FROM (VALUES (@@SERVERNAME)) AS server_name(server_name);
