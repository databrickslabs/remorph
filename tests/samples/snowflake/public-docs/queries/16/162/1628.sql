-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt

SELECT encrypt(to_binary(hex_encode('secret!')), 'sample_passphrase', NULL, 'aes-cbc/pad:pkcs') as encrypted_data;