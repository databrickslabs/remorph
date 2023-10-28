CREATE TABLE demonstration1 (
    ID INTEGER,
    array1 ARRAY,
    variant1 VARIANT,
    object1 OBJECT
    );

INSERT INTO demonstration1 (id, array1, variant1, object1) 
  SELECT 
    1, 
    ARRAY_CONSTRUCT(1, 2, 3), 
    PARSE_JSON(' { "key1": "value1", "key2": "value2" } '),
    PARSE_JSON(' { "outer_key1": { "inner_key1A": "1a", "inner_key1B": "1b" }, '
              ||
               '   "outer_key2": { "inner_key2": 2 } } ')
    ;

INSERT INTO demonstration1 (id, array1, variant1, object1) 
  SELECT 
    2,
    ARRAY_CONSTRUCT(1, 2, 3, NULL), 
    PARSE_JSON(' { "key1": "value1", "key2": NULL } '),
    PARSE_JSON(' { "outer_key1": { "inner_key1A": "1a", "inner_key1B": NULL }, '
              ||
               '   "outer_key2": { "inner_key2": 2 } '
              ||
               ' } ')
  ;