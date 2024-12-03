--Query type: DQL
SELECT DATEDIFF(microsecond, '1970-01-01 00:00:00', SYSDATETIME()) * 1.0 AS [System microseconds], [as of] FROM (VALUES (SYSDATETIME(), GETDATE())) AS SystemInfo(SystemTimeTicks, [as of]);
