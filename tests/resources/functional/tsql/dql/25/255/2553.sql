-- tsql sql:
WITH dates AS ( SELECT SYSDATETIME() AS date_value ) SELECT DATE_BUCKET( WEEK, 10, date_value ) AS bucketed_date FROM dates
