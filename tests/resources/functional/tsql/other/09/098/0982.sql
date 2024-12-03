--Query type: DDL
CREATE TABLE #AvroTable
(
    column1 INT,
    column2 VARCHAR(50)
);

INSERT INTO #AvroTable (column1, column2)
VALUES
    (1, 'Value1'),
    (2, 'Value2'),
    (3, 'Value3');

SELECT *
FROM #AvroTable;

-- REMORPH CLEANUP: DROP TABLE #AvroTable;
