-- Note that we cannot enable the WHERE clause here as teh python
-- tests will fail because SqlGlot cannot translate variable references
-- within strings. Enable the WHERE clause when we are not limited by Python

-- WHERE EMP_ID = '&empNo' =>  WHERE EMP_ID = '${empNo}'

-- snowflake sql:
select count(*) from &TEST_USER.EMP_TBL;

-- databricks sql:
select count(*) from $TEST_USER.EMP_TBL;
