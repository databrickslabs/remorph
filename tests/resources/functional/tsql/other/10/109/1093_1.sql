--Query type: DML
CREATE PROCEDURE dbo.TestProc
AS
    WITH TestCTE AS (
        SELECT TestCol = 1
    ),
    TestCTE2 AS (
        SELECT TestCol2 = 2
    )
    SELECT TestProcCol = T1.TestCol, T2.TestCol2
    FROM TestCTE T1
    CROSS JOIN TestCTE2 T2;
EXEC TestProc;
-- REMORPH CLEANUP: DROP PROCEDURE dbo.TestProc;
