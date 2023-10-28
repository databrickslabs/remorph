SELECT object_col,
       XMLGET(object_col, 'level2'),
       XMLGET(XMLGET(object_col, 'level2'), 'level3', 1)
    FROM xml_demo;