--Query type: DQL
WITH temp_result AS ( SELECT '     .#     test    .' AS str ) SELECT TRIM(TRAILING '.,! ' FROM str) AS Result FROM temp_result;
