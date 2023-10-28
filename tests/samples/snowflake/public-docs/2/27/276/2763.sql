SELECT xml_str, CHECK_XML(xml_str)
    FROM my_table
    WHERE CHECK_XML(xml_str) IS NOT NULL;