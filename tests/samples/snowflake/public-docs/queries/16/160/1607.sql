-- see https://docs.snowflake.com/en/sql-reference/functions/timestampadd

SELECT d AS "DATE", dateadd(year, 2, d) AS add_2_years, 
    dateadd(hour, 2, d) AS add_2_hours
  FROM datetest;