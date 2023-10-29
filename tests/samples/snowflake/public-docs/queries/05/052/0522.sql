-- see https://docs.snowflake.com/en/sql-reference/functions/sha2

CREATE TABLE sha_table(
    v VARCHAR, 
    v_as_sha1 VARCHAR,
    v_as_sha1_hex VARCHAR,
    v_as_sha1_binary BINARY,
    v_as_sha2 VARCHAR,
    v_as_sha2_hex VARCHAR,
    v_as_sha2_binary BINARY
    );
INSERT INTO sha_table(v) VALUES ('AbCd0');
UPDATE sha_table SET 
    v_as_sha1 = SHA1(v),
    v_as_sha1_hex = SHA1_HEX(v),
    v_as_sha1_binary = SHA1_BINARY(v),
    v_as_sha2 = SHA2(v),
    v_as_sha2_hex = SHA2_HEX(v),
    v_as_sha2_binary = SHA2_BINARY(v)
    ;