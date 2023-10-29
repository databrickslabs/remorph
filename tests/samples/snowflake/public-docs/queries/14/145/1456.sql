-- see https://docs.snowflake.com/en/sql-reference/functions/system_typeof

SELECT SYSTEM$TYPEOF('something') FROM (values(1)) v;
