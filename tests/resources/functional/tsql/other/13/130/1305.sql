-- tsql sql:
INSERT INTO dbo.doc_exy (column_a)
SELECT column_a
FROM (
    VALUES (10), (20), (30)
) AS temp (column_a);
