-- see https://docs.snowflake.com/en/sql-reference/functions/months_between

SELECT
    ROUND(MONTHS_BETWEEN('2019-03-31 12:00:00'::TIMESTAMP,
                         '2019-02-28 00:00:00'::TIMESTAMP)) AS MonthsBetween1;