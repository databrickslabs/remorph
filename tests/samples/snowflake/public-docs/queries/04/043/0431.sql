-- see https://docs.snowflake.com/en/sql-reference/functions/to_binary

CREATE TABLE binary_test (v VARCHAR, b BINARY);
INSERT INTO binary_test(v) VALUES ('SNOW');