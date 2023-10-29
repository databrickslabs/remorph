-- see https://docs.snowflake.com/en/sql-reference/functions/months_between

SELECT
    MONTHS_BETWEEN('2019-03-15'::DATE,
                   '2019-02-15'::DATE) AS MonthsBetween1,
    MONTHS_BETWEEN('2019-03-31'::DATE,
                   '2019-02-28'::DATE) AS MonthsBetween2;