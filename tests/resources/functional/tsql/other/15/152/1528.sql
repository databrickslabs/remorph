--Query type: DCL
DECLARE @cookie VARBINARY(8000);
DECLARE @customerID INT = 1;
EXECUTE AS USER = 'user1' WITH COOKIE INTO @cookie;
SELECT SUSER_NAME() AS CurrentUser, USER_NAME() AS UserName
FROM (
    VALUES (@customerID)
) AS ExecutionContext(ExecutionContext);
SELECT @cookie;
