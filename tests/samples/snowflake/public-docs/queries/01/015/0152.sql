-- see https://docs.snowflake.com/en/sql-reference/functions-date-time

ALTER SESSION SET WEEK_OF_YEAR_POLICY=1, WEEK_START=1;

SELECT d "Date", DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
FROM week_examples;


alter session set week_of_year_policy=1, week_start=3;

SELECT d "Date", DAYNAME(d) "Day",
       WEEK(d) "WOY",
       WEEKISO(d) "WOY (ISO)",
       YEAROFWEEK(d) "YOW",
       YEAROFWEEKISO(d) "YOW (ISO)"
FROM week_examples;
