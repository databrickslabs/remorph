--Query type: DML
DECLARE @myVariable AS VARCHAR(40);
SET @myVariable = 'This string is longer than thirty characters';
WITH myCTE AS (
    SELECT @myVariable AS myVariable
)
SELECT CAST(myVariable AS VARCHAR) AS myVariableCast,
       DATALENGTH(CAST(myVariable AS VARCHAR)) AS myVariableLength,
       CONVERT(CHAR, myVariable) AS myVariableConvert,
       DATALENGTH(CONVERT(CHAR, myVariable)) AS myVariableConvertLength
FROM myCTE