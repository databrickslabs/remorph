CREATE TABLE xml_03 (object_col_1 OBJECT);
INSERT INTO xml_03 (object_col_1)
    SELECT OBJECT_CONSTRUCT('key1', 'value1', 'key2', 'value2');