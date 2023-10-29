-- see https://docs.snowflake.com/en/sql-reference/data-types-logical

SELECT b, n, NOT b AND (n < 1) FROM test_boolean;
