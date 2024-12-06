-- tsql sql:
CREATE PROCEDURE usp_NewProc
AS
BEGIN
    SELECT 'Procedure created' AS Message;
END
-- REMORPH CLEANUP: DROP PROCEDURE usp_NewProc;
DECLARE @Message VARCHAR(50);
EXEC usp_NewProc;
SET @Message = 'Procedure executed';
SELECT Status FROM (VALUES (@Message)) AS ProcResult(Status);
