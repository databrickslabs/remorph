-- see https://docs.snowflake.com/en/sql-reference/functions/check_xml

SELECT xml_str, CHECK_XML(xml_str)
    FROM my_table
    WHERE CHECK_XML(xml_str) IS NOT NULL;