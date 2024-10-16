--Query type: DDL
DECLARE @AssemblyExists INT;

WITH AssemblyCheck AS (
    SELECT name
    FROM sys.assemblies
    WHERE name = 'MockAssembly'
)

SELECT @AssemblyExists = COUNT(*)
FROM AssemblyCheck;

IF @AssemblyExists > 0
BEGIN
    ALTER ASSEMBLY MockAssembly FROM 'C:\UpdatedMockAssembly.dll';
    PRINT 'Assembly altered successfully.';
END
ELSE
BEGIN
    PRINT 'Assembly does not exist.';
END

SELECT 'Query execution completed.' AS Message;