-- see https://docs.snowflake.com/en/sql-reference/functions/to_xml

SELECT array_col_1,
       TO_XML(array_col_1)
    FROM xml_04;