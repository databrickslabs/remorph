CREATE TABLE t1 (vo VARIANT);
INSERT INTO t1 (vo) 
    SELECT PARSE_JSON('{"a":1}');