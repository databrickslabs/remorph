-- see https://docs.snowflake.com/en/sql-reference/functions/datediff

SELECT DATEDIFF(year, '2010-04-09 14:39:20'::TIMESTAMP, 
                      '2013-05-08 23:39:20'::TIMESTAMP) 
               AS diff_years;