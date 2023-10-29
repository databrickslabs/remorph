-- see https://docs.snowflake.com/en/sql-reference/functions/to_xml

SELECT x, TO_VARCHAR(x), TO_XML(x)
    FROM xml2;