--Query type: DDL
DECLARE @TempResult TABLE (Col1 INT CHECK (Col1 > 100), Col2 INT);
INSERT INTO @TempResult (Col1, Col2)
VALUES (101, 200), (102, 150), (103, 250);
SELECT * FROM @TempResult;