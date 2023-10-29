-- see https://docs.snowflake.com/en/sql-reference/functions/parse_xml

SELECT PARSE_XML(STR => '<test>22257e111</test>', DISABLE_AUTO_CONVERT => TRUE);