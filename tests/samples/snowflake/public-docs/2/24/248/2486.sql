CREATE TABLE xml_04 (array_col_1 ARRAY);
INSERT INTO xml_04 (array_col_1)
    SELECT ARRAY_CONSTRUCT('v1', 'v2');