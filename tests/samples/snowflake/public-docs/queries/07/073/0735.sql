-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt

SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('Patient tested positive for COVID-19', $passphrase),
            $passphrase),
        'utf-8')
        AS dcrypt
    ;