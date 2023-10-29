-- see https://docs.snowflake.com/en/sql-reference/functions/decrypt_raw

UPDATE binary_table SET encrypted_binary_column =
    ENCRYPT_RAW(binary_column, 
        encryption_key, 
        initialization_vector, 
        aad_column,
        'AES-GCM');