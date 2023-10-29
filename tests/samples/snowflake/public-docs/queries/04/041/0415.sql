-- see https://docs.snowflake.com/en/sql-reference/session-variables

CREATE TABLE IDENTIFIER($MY_TABLE_NAME) (i INTEGER);
INSERT INTO IDENTIFIER($MY_TABLE_NAME) (i) VALUES (42);