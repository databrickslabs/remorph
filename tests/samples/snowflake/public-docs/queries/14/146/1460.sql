-- see https://docs.snowflake.com/en/sql-reference/functions/system_typeof

SELECT SYSTEM$TYPEOF(CONCAT('every', 'body')) FROM (values(1)) v;
