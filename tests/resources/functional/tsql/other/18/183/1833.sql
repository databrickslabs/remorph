-- tsql sql:
DECLARE @myid UNIQUEIDENTIFIER;
SET @myid = 'A972C577-DFB0-064E-1189-0154C99310DAAC12';
SELECT myid FROM (VALUES (@myid)) AS temp_result_set(myid);
