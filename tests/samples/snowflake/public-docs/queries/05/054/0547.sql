-- see https://docs.snowflake.com/en/sql-reference/sql/merge

CREATE TABLE target_table (ID INTEGER, description VARCHAR);

CREATE TABLE source_table (ID INTEGER, description VARCHAR);