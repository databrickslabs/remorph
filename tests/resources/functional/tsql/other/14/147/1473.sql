-- tsql sql:
WITH ManagerCTE AS (
    SELECT OrgNode, LoginID
    FROM (
        VALUES ('/1/', 'adventure-works\terri0'),
               ('/2/', 'adventure-works\rob0')
    ) AS EmployeeDemo(OrgNode, LoginID)
),
EmployeeCTE AS (
    SELECT OrgNode, LoginID
    FROM (
        VALUES ('/1/1/', 'adventure-works\rob1'),
               ('/2/2/', 'adventure-works\rob2')
    ) AS EmployeeDemo(OrgNode, LoginID)
)
SELECT CASE
        WHEN EmployeeCTE.OrgNode LIKE ManagerCTE.OrgNode + '%' THEN 'LoginID ' + EmployeeCTE.LoginID + ' is a subordinate of the selected Manager.'
        ELSE 'LoginID ' + EmployeeCTE.LoginID + ' is not a subordinate of the selected Manager.'
    END AS Result
FROM ManagerCTE
CROSS JOIN EmployeeCTE;

SELECT *
FROM ManagerCTE;

SELECT *
FROM EmployeeCTE;

-- REMORPH CLEANUP: DROP TABLE ManagerCTE;
-- REMORPH CLEANUP: DROP TABLE EmployeeCTE;
