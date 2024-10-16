--Query type: TCL
WITH backup_info AS ( SELECT 'customer' AS database_name, 'customer_backups' AS backup_name, 3 AS file_number, 'Jan 10, 2022 10:00 AM' AS stop_at ) SELECT * FROM backup_info