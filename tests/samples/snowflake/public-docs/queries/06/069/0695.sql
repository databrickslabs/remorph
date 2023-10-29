-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

INSERT INTO varia (v) 
    SELECT TO_VARIANT(PARSE_JSON('{"key3": "value3", "key4": "value4"}'));