-- see https://docs.snowflake.com/en/sql-reference/functions/system_stream_backlog

SELECT * FROM TABLE(SYSTEM$STREAM_BACKLOG('db1.schema1.s1'));