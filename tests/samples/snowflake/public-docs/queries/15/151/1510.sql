-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

SELECT TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'mm/dd/yyyy hh24:mi:ss');

SELECT TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'dd/mm/yyyy hh24:mi:ss');