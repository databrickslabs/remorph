--Query type: DQL
CREATE TABLE #temp_result (LocationID INT, LocationName VARCHAR(50));
INSERT INTO #temp_result (LocationID, LocationName)
VALUES (1, 'Location1'), (2, 'Location2');

SELECT 
    INDEXKEY_PROPERTY(OBJECT_ID('#temp_result', 'U'), 1, 1, 'ColumnId') AS [Column ID],
    INDEXKEY_PROPERTY(OBJECT_ID('#temp_result', 'U'), 1, 1, 'IsDescending') AS [Asc or Desc order];

-- REMORPH CLEANUP: DROP TABLE #temp_result;