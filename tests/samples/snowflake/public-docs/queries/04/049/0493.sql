-- see https://docs.snowflake.com/en/sql-reference/functions/is_array

CREATE TABLE multiple_types (
    array1 VARIANT,
    array2 VARIANT,
    boolean1 VARIANT,
    char1 VARIANT,
    varchar1 VARIANT,
    decimal1 VARIANT,
    double1 VARIANT,
    integer1 VARIANT,
    object1 VARIANT
    );
INSERT INTO multiple_types 
     (array1, array2, boolean1, char1, varchar1, 
      decimal1, double1, integer1, object1)
   SELECT 
     TO_VARIANT(TO_ARRAY('Example')), 
     TO_VARIANT(ARRAY_CONSTRUCT('Array-like', 'example')), 
     TO_VARIANT(TRUE), 
     TO_VARIANT('X'), 
     TO_VARIANT('I am a real character'), 
     TO_VARIANT(1.23::DECIMAL(6, 3)),
     TO_VARIANT(3.21::DOUBLE),
     TO_VARIANT(15),
     TO_VARIANT(TO_OBJECT(PARSE_JSON('{"Tree": "Pine"}')))
     ;