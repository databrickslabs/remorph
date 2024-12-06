-- tsql sql:
SELECT TOP (1) DATEPART(day, '12/20/1974') AS day_part FROM (VALUES ('12/20/1974')) AS customer (birth_date);
