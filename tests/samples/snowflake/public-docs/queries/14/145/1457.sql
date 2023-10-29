-- see https://docs.snowflake.com/en/sql-reference/functions/system_typeof

SELECT SYSTEM$TYPEOF(1) FROM (values(1)) v;
