-- see https://docs.snowflake.com/en/sql-reference/functions/decompress_string

SELECT DECOMPRESS_STRING(TO_BINARY('0920536E6F77666C616B65', 'HEX'), 'SNAPPY');