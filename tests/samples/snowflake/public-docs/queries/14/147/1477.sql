-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

SELECT TO_DATE ('2019-02-28') + INTERVAL '1 day, 1 year';


SELECT TO_DATE ('2019-02-28') + INTERVAL '1 year, 1 day';
