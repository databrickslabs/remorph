-- see https://docs.snowflake.com/en/sql-reference/functions/is_database_role_in_session

SELECT *
FROM myb.s1.t1
WHERE IS_DATABASE_ROLE_IN_SESSION(role_name);