-- tsql sql:
WITH temp_result AS (SELECT 0x25F18060 AS seed)
SELECT CRYPT_GEN_RANDOM(4, seed)
FROM temp_result;
