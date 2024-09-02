--Query type: DML
CREATE PROCEDURE my_sp_who
AS
BEGIN
    WITH dummy AS (
        SELECT 'Current Connections' AS [Status], 1 AS [Count]
    )
    SELECT [Status], [Count]
    FROM dummy;
END;

DECLARE @proc_name NVARCHAR(30);
SET @proc_name = 'my_sp_who';
EXEC @proc_name;
EXEC my_sp_who;
-- REMORPH CLEANUP: DROP PROCEDURE my_sp_who;