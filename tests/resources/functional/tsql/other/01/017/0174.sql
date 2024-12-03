--Query type: DDL
SELECT *
INTO #temp_result
FROM (
    VALUES ('1', '2', '3'),
           ('4', '5', '6')
) AS t (c1, c2, c3);

CREATE TABLE #temp_result_search_optimization (
    c1 nvarchar(10),
    c2 nvarchar(10),
    c3 nvarchar(10)
);

INSERT INTO #temp_result_search_optimization (c1, c2, c3)
SELECT c1, c2, c3
FROM #temp_result;

CREATE INDEX idx_c1
ON #temp_result_search_optimization (c1);

CREATE INDEX idx_c2_c3
ON #temp_result_search_optimization (c2, c3);

SELECT *
FROM #temp_result_search_optimization;

-- REMORPH CLEANUP: DROP TABLE #temp_result_search_optimization;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
