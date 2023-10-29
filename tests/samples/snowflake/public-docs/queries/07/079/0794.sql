-- see https://docs.snowflake.com/en/sql-reference/functions/time_slice

SELECT '2019-02-28'::DATE AS "DATE",
       TIME_SLICE("DATE", 4, 'MONTH', 'START') AS "START OF SLICE",
       TIME_SLICE("DATE", 4, 'MONTH', 'END') AS "END OF SLICE";