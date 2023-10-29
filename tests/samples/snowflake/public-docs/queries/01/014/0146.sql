-- see https://docs.snowflake.com/en/sql-reference/functions/current_time

ALTER SESSION SET TIME_OUTPUT_FORMAT = 'HH24:MI:SS.FF';

SELECT CURRENT_TIME(2);


SELECT CURRENT_TIME(4);


SELECT CURRENT_TIME;
