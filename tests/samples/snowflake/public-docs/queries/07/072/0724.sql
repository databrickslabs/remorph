-- see https://docs.snowflake.com/en/sql-reference/functions/months_between

SELECT
    MONTHS_BETWEEN('2019-03-01'::DATE,
                   '2019-02-15'::DATE) AS MonthsBetween1,
    MONTHS_BETWEEN('2019-03-01 02:00:00'::TIMESTAMP,
                   '2019-02-15 01:00:00'::TIMESTAMP) AS MonthsBetween2,
    MONTHS_BETWEEN('2019-02-15 02:00:00'::TIMESTAMP,
                   '2019-02-15 01:00:00'::TIMESTAMP) AS MonthsBetween3
    ;