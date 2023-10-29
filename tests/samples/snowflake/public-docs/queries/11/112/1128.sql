-- see https://docs.snowflake.com/en/sql-reference/functions/dayname

SELECT DAYNAME(TO_TIMESTAMP_NTZ('2015-05-02 10:00')) AS DAY;