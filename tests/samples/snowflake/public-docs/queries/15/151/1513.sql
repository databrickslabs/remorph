-- see https://docs.snowflake.com/en/sql-reference/functions/md5_binary

SELECT TO_VARCHAR(b, 'HEX') AS hex_representation
    FROM binary_demo;