-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt_raw

CREATE OR REPLACE TABLE binary_table (
    encryption_key BINARY,   -- DO NOT STORE REAL ENCRYPTION KEYS THIS WAY!
    initialization_vector BINARY(12), -- DO NOT STORE REAL IV'S THIS WAY!!
    binary_column BINARY,
    encrypted_binary_column VARIANT,
    aad_column BINARY);

INSERT INTO binary_table (encryption_key,
                          initialization_vector,
                          binary_column,
                          aad_column)
    SELECT SHA2_BINARY('NotSecretEnough', 256),
            SUBSTR(TO_BINARY(HEX_ENCODE('AlsoNotSecretEnough'), 'HEX'), 0, 12),
            TO_BINARY(HEX_ENCODE('Bonjour'), 'HEX'),
            TO_BINARY(HEX_ENCODE('additional data'), 'HEX')
    ;