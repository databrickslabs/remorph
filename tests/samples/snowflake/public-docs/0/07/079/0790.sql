SELECT 'Hello' as original_value,
       binary_column, 
       hex_decode_string(to_varchar(binary_column)) as decoded,
       -- encrypted_binary_column,
       decrypt(encrypted_binary_column, 'SamplePassphrase') as decrypted,
       hex_decode_string(to_varchar(decrypt(encrypted_binary_column, 'SamplePassphrase'))) as decrypted_and_decoded
    FROM binary_table;