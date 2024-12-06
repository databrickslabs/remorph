-- tsql sql:
WITH dates AS ( SELECT CAST('1992-01-01' AS datetime) AS start_date, CAST('1992-01-02' AS datetime) AS end_date ) SELECT DATEDIFF(day, start_date, end_date) FROM dates
