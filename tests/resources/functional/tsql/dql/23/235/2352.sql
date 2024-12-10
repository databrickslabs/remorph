-- tsql sql:
SELECT * FROM (VALUES ('E-D-C-B-A')) AS t(str) CROSS APPLY STRING_SPLIT(t.str, '-', 1) AS s ORDER BY s.value DESC
