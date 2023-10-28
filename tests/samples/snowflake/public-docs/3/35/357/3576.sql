INSERT INTO varia (v) 
    SELECT TO_VARIANT(PARSE_JSON('{"key3": "value3", "key4": "value4"}'));