-- see https://docs.snowflake.com/en/sql-reference/functions/is_role_in_session

SELECT IS_ROLE_IN_SESSION(UPPER(authz_role)) FROM t1;