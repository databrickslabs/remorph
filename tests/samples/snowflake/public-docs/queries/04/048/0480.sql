-- see https://docs.snowflake.com/en/sql-reference/functions/to_json

CREATE TABLE jdemo1 (v VARIANT);
INSERT INTO jdemo1 SELECT PARSE_JSON('{"food":"bard"}');