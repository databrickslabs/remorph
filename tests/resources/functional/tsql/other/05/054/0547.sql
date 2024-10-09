--Query type: DDL
CREATE TABLE #FG_SALES
(
    DataID INT,
    DataValue VARCHAR(100)
);

INSERT INTO #FG_SALES (DataID, DataValue)
VALUES
    (1, 'Sales Data 1'),
    (2, 'Sales Data 2');

SELECT *
FROM #FG_SALES;

DROP TABLE #FG_SALES;