--Query type: DDL
CREATE TABLE #CustomerTemp
(
    LastName VARCHAR(50)
);

INSERT INTO #CustomerTemp
(
    LastName
)
VALUES
(
    'Smith',
    'Johnson',
    'Williams'
);

CREATE STATISTICS #CustomerTemp_LastName
ON #CustomerTemp
(
    LastName
);

SELECT *
FROM #CustomerTemp;

-- REMORPH CLEANUP: DROP TABLE #CustomerTemp;
-- REMORPH CLEANUP: DROP STATISTICS #CustomerTemp_LastName;
