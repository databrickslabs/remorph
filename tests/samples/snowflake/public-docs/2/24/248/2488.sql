CREATE TABLE xml_05 (json_col_1 VARIANT);
INSERT INTO xml_05 (json_col_1)
    SELECT PARSE_JSON(' { "key1": ["a1", "a2"] } ');