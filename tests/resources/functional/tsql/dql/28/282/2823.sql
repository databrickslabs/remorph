-- tsql sql:
SELECT TRIM('.,! ' FROM '     #     test    .') AS Result FROM (VALUES ('     #     test    .')) AS T1(Column1);