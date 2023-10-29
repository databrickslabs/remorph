-- see https://docs.snowflake.com/en/sql-reference/functions/year

SELECT 
       '2016-01-02T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       DAYOFWEEK(tstamp) AS "DAY OF WEEK",
       DAYOFWEEKISO(tstamp) AS "DAY OF WEEK ISO"
       ;