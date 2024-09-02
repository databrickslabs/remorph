--Query type: DML
INSERT INTO V1
SELECT *
FROM (
    VALUES ('Row 1', 1),
           ('Row 2', 2)
) AS T (Col1, Col2);