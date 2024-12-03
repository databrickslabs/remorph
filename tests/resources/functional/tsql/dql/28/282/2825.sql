--Query type: DQL
SELECT TRIM(LEADING '.,! ' FROM '     .#     test    .') AS Result FROM (VALUES ('     .#     test    .')) AS T1 (Column1);
