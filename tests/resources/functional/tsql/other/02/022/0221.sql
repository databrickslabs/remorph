-- tsql sql:
SELECT CASE WHEN flag = 1 THEN 'Notification muted' ELSE 'Notification not muted' END AS notification_status FROM (VALUES (1)) AS temp_table (flag);
