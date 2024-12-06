-- tsql sql:
SELECT t.* FROM (VALUES (1, 'Product1'), (2, 'Product2'), (3, 'Product3')) AS t (ProductKey, Name) ORDER BY Name ASC;
