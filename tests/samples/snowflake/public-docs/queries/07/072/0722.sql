-- see https://docs.snowflake.com/en/sql-reference/functions/encrypt

SELECT
    DECRYPT(
        ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
        $passphrase, 'wrong patient AAD', 'aes-gcm') AS medicine
    ;