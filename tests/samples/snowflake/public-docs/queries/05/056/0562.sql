-- see https://docs.snowflake.com/en/sql-reference/functions/xmlget

CREATE TABLE xml_demo (ID INTEGER, object_col OBJECT);
INSERT INTO xml_demo (id, object_col)
    SELECT 1001,
        PARSE_XML('<level1> 1 <level2> 2 <level3> 3A </level3> <level3> 3B </level3> </level2> </level1>');