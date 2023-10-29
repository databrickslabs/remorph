-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

CREATE PROCEDURE FindEmployee @EmpLName CHAR(20)
AS
SELECT @EmpLName = RTRIM(@EmpLName) + '%';

SELECT p.FirstName,
    p.LastName,
    a.City
FROM Person.Person p
INNER JOIN Person.Address a
    ON p.BusinessEntityID = a.AddressID
WHERE p.LastName LIKE @EmpLName;
GO

EXEC FindEmployee @EmpLName = 'Barb';
GO