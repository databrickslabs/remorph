-- see https://docs.snowflake.com/en/sql-reference/functions/datediff

SELECT DATEDIFF(hour, '2013-05-08T23:39:20.123-07:00'::TIMESTAMP, 
    DATEADD(year, 2, ('2013-05-08T23:39:20.123-07:00')::TIMESTAMP)) 
               AS diff_hours;