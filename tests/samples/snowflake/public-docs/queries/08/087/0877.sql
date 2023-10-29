-- see https://docs.snowflake.com/en/sql-reference/functions/validate

SELECT * FROM TABLE(VALIDATE(t1, JOB_ID => '_last'));