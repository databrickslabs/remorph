-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

SELECT CAST('2022-04-01' AS DATE);

SELECT '2022-04-01'::DATE;

SELECT TO_DATE('2022-04-01');