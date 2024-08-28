-- this example will fail until we implement the macro translation engine, because
-- it is how snowsql is resolving variables in the sql script.

-- snowflake sql:
select count(*) from &TEST_USER.EMP_TBL;

-- databricks sql:
select count(*) from $TEST_USER.EMP_TBL;
