SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('Patient tested positive for COVID-19', $passphrase),
            $passphrase),
        'utf-8')
        AS dcrypt
    ;