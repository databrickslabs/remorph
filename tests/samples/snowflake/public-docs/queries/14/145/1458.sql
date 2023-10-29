-- see https://docs.snowflake.com/en/sql-reference/functions/system_typeof

SELECT SYSTEM$TYPEOF(10000) FROM (values(1)) v;
