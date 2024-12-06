-- tsql sql:
SELECT DATEDIFF(millisecond, current_dt, system_dt) FROM (VALUES (GETDATE(), SYSDATETIME())) AS dates (current_dt, system_dt);
