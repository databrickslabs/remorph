-- see https://docs.snowflake.com/en/sql-reference/functions/parse_url

SELECT PARSE_URL('example.int/hello.php?user=12#nofragment', 0);