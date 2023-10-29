-- see https://docs.snowflake.com/en/sql-reference/functions/decrypt_raw

SELECT 'Bonjour' as original_value,
       binary_column,
       hex_decode_string(to_varchar(binary_column)) as decoded,
       encrypted_binary_column,
       decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
                  encryption_key,
                  as_binary(get(encrypted_binary_column, 'iv')),
                  aad_column,
                  'AES-GCM',
                  as_binary(get(encrypted_binary_column, 'tag')))
           as decrypted,
       hex_decode_string(to_varchar(decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
                  encryption_key,
                  as_binary(get(encrypted_binary_column, 'iv')),
                  aad_column,
                  'AES-GCM',
                  as_binary(get(encrypted_binary_column, 'tag')))
                  ))
           as decrypted_and_decoded
    FROM binary_table;