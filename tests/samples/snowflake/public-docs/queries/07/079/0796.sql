-- see https://docs.snowflake.com/en/sql-reference/functions/reverse

SELECT '2019-05-22'::DATE, REVERSE('2019-05-22'::DATE) AS reversed;