INSERT INTO xml_demo (id, object_col)
    SELECT 1002,
        PARSE_XML('<level1> 1 <level2 an_attribute="my attribute"> 2 </level2> </level1>');