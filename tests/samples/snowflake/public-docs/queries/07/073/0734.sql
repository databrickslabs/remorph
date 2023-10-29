-- see https://docs.snowflake.com/en/sql-reference/functions/decrypt

SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('Patient tested positive for COVID-19', $passphrase),
            $passphrase),
        'utf-8')
        AS dcrypt
    ;