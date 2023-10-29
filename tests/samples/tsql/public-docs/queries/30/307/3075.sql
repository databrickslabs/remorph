-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

CREATE FUNCTION dbo.GetContactInformation (@BusinessEntityID INT)
RETURNS @retContactInformation TABLE (
    BusinessEntityID INT NOT NULL,
    FirstName NVARCHAR(50) NULL,
    LastName NVARCHAR(50) NULL,
    ContactType NVARCHAR(50) NULL,
    PRIMARY KEY CLUSTERED (BusinessEntityID ASC)
    )
AS
-- Returns the first name, last name and contact type for the specified contact.
BEGIN
    DECLARE @FirstName NVARCHAR(50),
        @LastName NVARCHAR(50),
        @ContactType NVARCHAR(50);

    -- Get common contact information
    SELECT @BusinessEntityID = BusinessEntityID,
        @FirstName = FirstName,
        @LastName = LastName
    FROM Person.Person
    WHERE BusinessEntityID = @BusinessEntityID;

    SET @ContactType = CASE
            -- Check for employee
            WHEN EXISTS (
                    SELECT *
                    FROM HumanResources.Employee AS e
                    WHERE e.BusinessEntityID = @BusinessEntityID
                    )
                THEN 'Employee'
                    -- Check for vendor
            WHEN EXISTS (
                    SELECT *
                    FROM Person.BusinessEntityContact AS bec
                    WHERE bec.BusinessEntityID = @BusinessEntityID
                    )
                THEN 'Vendor'
                    -- Check for store
            WHEN EXISTS (
                    SELECT *
                    FROM Purchasing.Vendor AS v
                    WHERE v.BusinessEntityID = @BusinessEntityID
                    )
                THEN 'Store Contact'
                    -- Check for individual consumer
            WHEN EXISTS (
                    SELECT *
                    FROM Sales.Customer AS c
                    WHERE c.PersonID = @BusinessEntityID
                    )
                THEN 'Consumer'
            END;

    -- Return the information to the caller
    IF @BusinessEntityID IS NOT NULL
    BEGIN
        INSERT @retContactInformation
        SELECT @BusinessEntityID,
            @FirstName,
            @LastName,
            @ContactType;
    END;

    RETURN;
END;
GO

SELECT BusinessEntityID,
    FirstName,
    LastName,
    ContactType
FROM dbo.GetContactInformation(2200);
GO

SELECT BusinessEntityID,
    FirstName,
    LastName,
    ContactType
FROM dbo.GetContactInformation(5);
GO