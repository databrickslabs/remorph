--Query type: DDL
CREATE PROCEDURE dbo.usp_NewDemo
WITH EXECUTE AS 'CompanyDomain\SqlUser2'
AS
SELECT user_name() AS [current_user]
FROM (VALUES (1)) AS temp_table(id);
-- REMORPH CLEANUP: DROP PROCEDURE dbo.usp_NewDemo;