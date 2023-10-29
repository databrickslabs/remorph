-- see https://docs.snowflake.com/en/sql-reference/functions/to_xml

SELECT json_col_1,
       TO_JSON(json_col_1),
       TO_XML(json_col_1)
    FROM xml_05;