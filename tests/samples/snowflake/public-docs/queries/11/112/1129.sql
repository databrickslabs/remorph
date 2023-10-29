-- see https://docs.snowflake.com/en/sql-reference/functions/decompress_binary

SELECT DECOMPRESS_BINARY(TO_BINARY('0920536E6F77666C616B65', 'HEX'), 'SNAPPY');