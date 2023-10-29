-- see https://docs.snowflake.com/en/sql-reference/functions/parse_xml

SELECT PARSE_XML('<test>22257e111</test>'), PARSE_XML('<test>22257e111</test>', TRUE);