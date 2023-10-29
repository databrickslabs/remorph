-- see https://docs.snowflake.com/en/sql-reference/constructs/from

SELECT FILE_URL FROM DIRECTORY(@mystage) WHERE SIZE > 100000;