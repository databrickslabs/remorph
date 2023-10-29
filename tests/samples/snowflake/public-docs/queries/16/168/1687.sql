-- see https://docs.snowflake.com/en/sql-reference/functions/xmlget

SELECT object_col,
       GET(XMLGET(object_col, 'level2'), '@an_attribute')
    FROM xml_demo
    WHERE ID = 1002;