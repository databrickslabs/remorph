-- see https://docs.snowflake.com/en/sql-reference/functions/hash

SELECT HASH(null), HASH(null, null), HASH(null, null, null);
