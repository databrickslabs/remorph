-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt

SELECT encrypt(to_binary(hex_encode('Secret!')), 'SamplePassphrase', to_binary(hex_encode('Authenticated Data')));