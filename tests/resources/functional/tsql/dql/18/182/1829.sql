--Query type: DQL
DECLARE @myVariable AS VARCHAR = 'abc';
DECLARE @myNextVariable AS CHAR = 'abc';

SELECT DATALENGTH(myVariable) AS length_myVariable, DATALENGTH(myNextVariable) AS length_myNextVariable
FROM (
    VALUES (@myVariable, @myNextVariable)
) AS myValues(myVariable, myNextVariable);
