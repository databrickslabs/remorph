-- see https://docs.snowflake.com/en/sql-reference/functions/to_object

CREATE TABLE t1 (vo VARIANT);
INSERT INTO t1 (vo) 
    SELECT PARSE_JSON('{"a":1}');