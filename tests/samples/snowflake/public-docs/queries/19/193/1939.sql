-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt_raw

WITH
    decrypted_but_not_decoded as (
        decrypt_raw(as_binary(get(encrypted_binary_column, 'ciphertext')),
                      encryption_key,
                      as_binary(get(encrypted_binary_column, 'iv')),
                      aad_column,
                      'AES-GCM',
                      as_binary(get(encrypted_binary_column, 'tag')))
    )
SELECT 'Bonjour' as original_value,
       binary_column,
       hex_decode_string(to_varchar(binary_column)) as decoded,
       encrypted_binary_column,
       decrypted_but_not_decoded,
       hex_decode_string(to_varchar(decrypted_but_not_decoded))
           as decrypted_and_decoded
    FROM binary_table;