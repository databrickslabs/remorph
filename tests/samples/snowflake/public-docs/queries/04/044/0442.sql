-- see https://docs.snowflake.com/en/sql-reference/functions/collation

CREATE TABLE collation1 (v VARCHAR COLLATE 'sp');
INSERT INTO collation1 (v) VALUES ('ñ');