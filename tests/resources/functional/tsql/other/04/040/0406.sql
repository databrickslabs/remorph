--Query type: DDL
WITH AlertNotifications AS ( SELECT 'Alert 1' AS AlertMessage, 'High' AS Severity UNION ALL SELECT 'Alert 2', 'Medium' UNION ALL SELECT 'Alert 3', 'Low' ) SELECT * FROM AlertNotifications;
