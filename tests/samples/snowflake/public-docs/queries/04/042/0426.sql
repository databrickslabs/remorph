-- see https://docs.snowflake.com/en/sql-reference/functions/md5_binary

CREATE TABLE binary_demo (b BINARY);
INSERT INTO binary_demo (b) SELECT MD5_BINARY('Snowflake');