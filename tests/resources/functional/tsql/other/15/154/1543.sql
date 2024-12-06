-- tsql sql:
SELECT 'Week-6', DATETRUNC(week, d) FROM (VALUES (CAST('2022-01-01' AS DATE))) AS t(d);
