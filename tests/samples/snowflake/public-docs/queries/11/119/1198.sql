-- see https://docs.snowflake.com/en/sql-reference/functions/hash

SELECT HASH(SEQ8()) FROM TABLE(GENERATOR(rowCount=>10));
