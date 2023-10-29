-- see https://docs.snowflake.com/en/sql-reference/functions/is_role_in_session

SELECT *
FROM myb.s1.t1
WHERE IS_ROLE_IN_SESSION(t1.role_name);