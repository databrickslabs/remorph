-- see https://docs.snowflake.com/en/sql-reference/functions/year

SELECT 
       '2016-01-02T23:39:20.123-07:00'::TIMESTAMP AS tstamp,
       WEEK(tstamp) AS "WEEK",
       WEEKISO(tstamp) AS "WEEK ISO",
       WEEKOFYEAR(tstamp) AS "WEEK OF YEAR",
       YEAROFWEEK(tstamp) AS "YEAR OF WEEK",
       YEAROFWEEKISO(tstamp) AS "YEAR OF WEEK ISO"
       ;