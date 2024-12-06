-- tsql sql:
CREATE TABLE #Users
(
    UserName nvarchar(50),
    UserLogin nvarchar(50)
);

INSERT INTO #Users (UserName, UserLogin)
VALUES ('WanidaBenshoof', 'AdvWorks\YoonM');

CREATE USER [WanidaBenshoof] FOR LOGIN [AdvWorks\YoonM];

GRANT IMPERSONATE ON USER::[WanidaBenshoof] TO [WanidaBenshoof];

REVOKE IMPERSONATE ON USER::[WanidaBenshoof] FROM [WanidaBenshoof];

SELECT * FROM #Users;

DROP TABLE #Users;

-- REMORPH CLEANUP: DROP USER [WanidaBenshoof];
