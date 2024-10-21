--Query type: DML
CREATE PROCEDURE dbo.usp_myproc2
    WITH EXECUTE AS CALLER
AS
BEGIN
    SELECT SUSER_NAME() AS system_username, USER_NAME() AS current_username;
    EXECUTE AS USER = 'guest';
    SELECT SUSER_NAME() AS system_username, USER_NAME() AS current_username;
    REVERT;
    SELECT SUSER_NAME() AS system_username, USER_NAME() AS current_username;
    SELECT *
    FROM (
        VALUES ('guest')
    ) AS mycte(username);
END