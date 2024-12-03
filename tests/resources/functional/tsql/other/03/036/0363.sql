--Query type: DDL
CREATE PROCEDURE usp_NewProc
AS
SELECT *
FROM (
VALUES (1, 'John'),
       (2, 'Doe')
) AS tempTable(id, name);
-- REMORPH CLEANUP: DROP PROCEDURE usp_NewProc;
