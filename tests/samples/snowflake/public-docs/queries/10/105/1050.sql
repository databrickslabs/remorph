-- see https://docs.snowflake.com/en/sql-reference/functions/check_xml

SELECT CHECK_XML('<name> Invalid </WRONG_CLOSING_TAG>');