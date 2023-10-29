-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver16

SELECT
    CAST('2022-05-08 12:35:29.1234567 +12:15' AS TIME(7)) AS 'time',
    CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATE) AS 'date',
    CAST('2022-05-08 12:35:29.123' AS SMALLDATETIME) AS 'smalldatetime',
    CAST('2022-05-08 12:35:29.123' AS DATETIME) AS 'datetime',
    CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATETIME2(7)) AS 'datetime2',
    CAST('2022-05-08 12:35:29.1234567 +12:15' AS DATETIMEOFFSET(7)) AS 'datetimeoffset';