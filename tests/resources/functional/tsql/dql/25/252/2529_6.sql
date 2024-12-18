-- tsql sql:
WITH dates AS ( SELECT CAST('2005-12-31 23:59:59.9999999' AS datetime) AS start_date, CAST('2006-01-01 00:00:00.0000000' AS datetime) AS end_date ) SELECT DATEDIFF(second, start_date, end_date) FROM dates
