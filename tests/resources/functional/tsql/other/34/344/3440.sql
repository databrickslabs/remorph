--Query type: DCL
SELECT * FROM (VALUES ('password1', 'password2'), ('password3', 'password4')) AS passwords (decryption_password, encryption_password);