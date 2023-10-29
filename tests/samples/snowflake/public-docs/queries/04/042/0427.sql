-- see https://docs.snowflake.com/en/sql-reference/functions/decrypt

CREATE TABLE binary_table (
    binary_column BINARY,
    encrypted_binary_column BINARY);
INSERT INTO binary_table (binary_column) 
    SELECT (TO_BINARY(HEX_ENCODE('Hello')));
UPDATE binary_table 
    SET encrypted_binary_column = ENCRYPT(binary_column, 'SamplePassphrase');