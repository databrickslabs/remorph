-- see https://docs.snowflake.com/en/sql-reference/functions/cleanup_database_role_grants

SELECT CLEANUP_DATABASE_ROLE_GRANTS('mydb.dbr1' , 'myshare');