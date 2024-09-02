--Query type: DML
CREATE TABLE #Table1
(
    ColA INT,
    ColB VARCHAR(50)
);

CREATE TABLE #Table2
(
    ColA INT,
    ColC VARCHAR(50)
);

INSERT INTO #Table1 (ColA, ColB)
VALUES
    (1, 'Value1'),
    (2, 'Value2');

INSERT INTO #Table2 (ColA, ColC)
VALUES
    (1, 'Value3'),
    (2, 'Value4');

DELETE t2
FROM #Table2 t2
INNER JOIN #Table1 t1 ON t2.ColA = t1.ColA
WHERE t2.ColA = 1;

SELECT *
FROM #Table1;

SELECT *
FROM #Table2;

-- REMORPH CLEANUP: DROP TABLE #Table1;
-- REMORPH CLEANUP: DROP TABLE #Table2;