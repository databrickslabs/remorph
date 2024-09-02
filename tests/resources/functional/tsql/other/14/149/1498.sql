--Query type: DML
DECLARE @SamplesPath nvarchar(1024);

WITH temp_result AS (
    SELECT 'Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\master.mdf' AS physical_name
)

SELECT @SamplesPath = REPLACE(
    physical_name
    , 'Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\master.mdf'
    , 'Microsoft SQL Server\130\Samples\Engine\Programmability\CLR\'
)

FROM temp_result

WHERE physical_name = 'Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\master.mdf';

CREATE ASSEMBLY [SurrogateStringFunction]
FROM @SamplesPath + 'StringManipulate\CS\StringManipulate\bin\debug\SurrogateStringFunction.dll'
WITH PERMISSION_SET = SAFE;

-- REMORPH CLEANUP: DROP ASSEMBLY [SurrogateStringFunction];