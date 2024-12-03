--Query type: DQL
WITH TempResult AS ( SELECT 1 AS Reads, 2 AS Writes )
SELECT Reads, Writes, GETDATE() AS [As of]
FROM TempResult;
