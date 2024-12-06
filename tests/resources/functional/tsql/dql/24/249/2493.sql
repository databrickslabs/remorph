-- tsql sql:
WITH temp_result AS ( SELECT 1 AS id ) SELECT CRYPT_GEN_RANDOM(50) AS random_value FROM temp_result;
