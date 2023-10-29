-- see https://docs.snowflake.com/en/sql-reference/functions/system_reference

CALL myprocedure( SYSTEM$REFERENCE('TABLE', 'table_with_different_owner', 'SESSION', 'INSERT'. 'UPDATE', 'TRUNCATE'));