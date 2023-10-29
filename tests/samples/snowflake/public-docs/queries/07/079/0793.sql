-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

SELECT '2017-01-01 12:00:00'::TIMESTAMP_TZ;


SELECT DATEADD(MONTH, 6, '2017-01-01 12:00:00'::TIMESTAMP_TZ);
