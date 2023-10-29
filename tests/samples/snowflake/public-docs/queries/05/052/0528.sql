-- see https://docs.snowflake.com/en/sql-reference/functions/try_to_binary

CREATE TABLE strings (v VARCHAR, hex_encoded_string VARCHAR, b BINARY);
INSERT INTO strings (v) VALUES
    ('01'),
    ('A B'),
    ('Hello'),
    (NULL);
UPDATE strings SET hex_encoded_string = HEX_ENCODE(v);
UPDATE strings SET b = TRY_TO_BINARY(hex_encoded_string, 'HEX');