-- tsql sql:
IF OBJECT_ID('binary_table_new', 'U') IS NOT NULL
    DROP TABLE binary_table_new;

CREATE TABLE binary_table_new
(
    encryption_key_new VARBINARY(MAX),
    initialization_vector_new VARBINARY(12),
    binary_column_new VARBINARY(MAX),
    encrypted_binary_column_new VARBINARY(MAX),
    aad_column_new VARBINARY(MAX)
);

INSERT INTO binary_table_new
    (
        encryption_key_new,
        initialization_vector_new,
        binary_column_new,
        aad_column_new
    )
SELECT
    CONVERT(VARBINARY(MAX), HASHBYTES('SHA2_256', 'NotSecretEnoughNew'), 2) AS encryption_key_new,
    CONVERT(VARBINARY(12), 'AlsoNotSecretEnoughNew', 2) AS initialization_vector_new,
    CONVERT(VARBINARY(MAX), 'BonjourNew', 2) AS binary_column_new,
    CONVERT(VARBINARY(MAX), 'additional dataNew', 2) AS aad_column_new
FROM
    (
        VALUES
            (
                1
            )
    ) AS temp_result (dummy);

SELECT * FROM binary_table_new;
-- REMORPH CLEANUP: DROP TABLE binary_table_new;
