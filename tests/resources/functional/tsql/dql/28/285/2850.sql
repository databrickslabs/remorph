-- tsql sql:
WITH dates AS ( SELECT CAST('1999-01-01' AS DATE) AS date_value ) SELECT YEAR(date_value), MONTH(date_value), DAY(date_value) FROM dates
