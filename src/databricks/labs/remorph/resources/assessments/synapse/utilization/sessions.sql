--- Sessions

SELECT *, CURRENT_TIMESTAMP as extract_ts
FROM SYS.DM_PDW_EXEC_SESSIONS
WHERE CHARINDEX('system', LOWER(login_name)) = 0 and login_time > '2000-01-01'

