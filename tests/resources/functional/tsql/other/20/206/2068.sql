--Query type: DML
WITH EmployeeCTE AS (
    SELECT EmployeeID, ContactID, ManagerID, Title
    FROM (
        VALUES (1, 1, 2, 'Title1'),
               (2, 2, 2, 'Title2')
    ) AS Employee (EmployeeID, ContactID, ManagerID, Title)
),
ContactCTE AS (
    SELECT ContactID, LastName, FirstName
    FROM (
        VALUES (1, 'LastName1', 'FirstName1'),
               (2, 'LastName2', 'FirstName2')
    ) AS Contact (ContactID, LastName, FirstName)
)
SELECT c.LastName, c.FirstName, e.Title
FROM EmployeeCTE e WITH (NOLOCK, INDEX (EmployeeID))
JOIN ContactCTE c ON e.ContactID = c.ContactID
WHERE e.ManagerID = 2
OPTION (TABLE HINT (e, NOLOCK));
