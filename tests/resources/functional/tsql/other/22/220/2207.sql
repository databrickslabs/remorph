-- tsql sql:
INSERT INTO dbo.t
SELECT *
FROM (
    VALUES
        (1, 'a'),
        (2, CONVERT(CHAR, 1))
) AS v(id, name);
