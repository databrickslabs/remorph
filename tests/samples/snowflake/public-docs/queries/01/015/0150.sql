-- see https://docs.snowflake.com/en/sql-reference/functions-date-time

ALTER SESSION SET WEEK_OF_YEAR_POLICY=0, WEEK_START=0;

SELECT d "Date", DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
FROM week_examples;
