SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
            $passphrase, 'John Dough AAD', 'aes-gcm'),
        'utf-8')
        AS medicine
    ;