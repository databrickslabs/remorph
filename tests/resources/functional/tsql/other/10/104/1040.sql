--Query type: DCL
CREATE TABLE #Logins
(
    LoginName sysname,
    PasswordHash varbinary(256)
);

INSERT INTO #Logins (LoginName, PasswordHash)
VALUES ('NewUser', HASHBYTES('SHA2_256', 'NewPassword'));

CREATE LOGIN [NewUser]
WITH PASSWORD = 'NewPassword';

SELECT *
FROM #Logins;

-- REMORPH CLEANUP: DROP TABLE #Logins;
-- REMORPH CLEANUP: DROP LOGIN [NewUser];