-- tsql sql:
SELECT CAST(V.value AS money) AS converted_value
FROM (VALUES (10.3496847)) AS V(value);
