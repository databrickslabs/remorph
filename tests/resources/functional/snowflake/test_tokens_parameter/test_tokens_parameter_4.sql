-- snowflake sql:
select count(*) from &TEST_USER.EMP_TBL WHERE EMP_ID = '&empNo';

-- databricks sql:
select count(*) from ${TEST_USER}.EMP_TBL WHERE EMP_ID = '${empNo}';
