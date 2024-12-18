-- tsql sql:
DECLARE @p TABLE (X decimal(10, 1), Y decimal(10, 1));
INSERT INTO @p (X, Y)
SELECT X, Y
FROM (
    VALUES (1.0, 2.0),
           (3.0, 4.0),
           (5.0, 6.0)
) AS Points(X, Y)
WHERE X = 1.0;
UPDATE @p
SET X = X + 1.1;
SELECT *
FROM @p;
SELECT *
FROM (
    VALUES (1.0, 2.0),
           (3.0, 4.0),
           (5.0, 6.0)
) AS Points(X, Y);
