-- tsql sql:
CREATE PROCEDURE usp_FindCustomer
    @lastname VARCHAR(40) = '%',
    @firstname VARCHAR(20) = '%'
AS
BEGIN
    DECLARE @Count INT;
    DECLARE @ProcName NVARCHAR(128);

    WITH CustomerCTE AS (
        SELECT FirstName, LastName
        FROM (
            VALUES ('John', 'Doe'),
                   ('Jane', 'Doe'),
                   ('Alice', 'Smith'),
                   ('Bob', 'Johnson')
        ) AS Customer(FirstName, LastName)
    )
    SELECT FirstName, LastName
    FROM CustomerCTE
    WHERE FirstName LIKE @firstname AND LastName LIKE @lastname;

    SET @Count = @@ROWCOUNT;
    SET @ProcName = OBJECT_NAME(@@PROCID);
    RAISERROR ('Stored procedure %s returned %d rows.', 16, 10, @ProcName, @Count);
END;
EXECUTE usp_FindCustomer 'D%', 'J%';
-- REMORPH CLEANUP: DROP PROCEDURE usp_FindCustomer;
