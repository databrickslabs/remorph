-- tsql sql:
CREATE TABLE Territory (TerritoryID INT, RegionID INT, Name NVARCHAR(50));
INSERT INTO Territory (TerritoryID, RegionID, Name)
VALUES (1, 1, 'North1'), (2, 1, 'North2'), (3, 2, 'South1'), (4, 2, 'South2');

BEGIN TRANSACTION;
BEGIN TRY
    WITH TerritoryCTE (TerritoryID, RegionID, Name)
    AS (
        SELECT 1, 1, 'North1'
        UNION ALL
        SELECT 2, 1, 'North2'
        UNION ALL
        SELECT 3, 2, 'South1'
        UNION ALL
        SELECT 4, 2, 'South2'
    )
    UPDATE t
    SET t.Name = N'MyNewName'
    FROM Territory t
    INNER JOIN TerritoryCTE cte ON t.TerritoryID = cte.TerritoryID
    WHERE cte.TerritoryID BETWEEN 1 AND 2;

    INSERT INTO Territory (TerritoryID, RegionID, Name)
    SELECT TerritoryID, RegionID, Name
    FROM TerritoryCTE;

    SELECT * FROM Territory;
END TRY
BEGIN CATCH
    SELECT ERROR_NUMBER() AS ErrorNumber,
           ERROR_SEVERITY() AS ErrorSeverity,
           ERROR_STATE() AS ErrorState,
           ERROR_PROCEDURE() AS ErrorProcedure,
           ERROR_LINE() AS ErrorLine,
           ERROR_MESSAGE() AS ErrorMessage;

    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
END CATCH;

IF @@TRANCOUNT > 0
    COMMIT TRANSACTION;

-- REMORPH CLEANUP: DROP TABLE Territory;
