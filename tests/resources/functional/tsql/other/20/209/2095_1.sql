--Query type: DML
CREATE PROCEDURE Sales.uspGetCustomers
    @FirstName nvarchar(50),
    @LastName nvarchar(50)
AS
BEGIN
    WITH Customers AS (
        SELECT *
        FROM (
            VALUES
                (1, 'Pilar', 'Ackerman', 'pilar0@adventure-works.com'),
                (2, 'Linda', 'Chen', 'linda1@adventure-works.com'),
                (3, 'David', 'Smith', 'david2@adventure-works.com')
        ) c (CustomerID, FirstName, LastName, EmailAddress)
    )
    SELECT c.CustomerID, c.FirstName, c.LastName, c.EmailAddress
    FROM Customers c
    WHERE c.FirstName = @FirstName AND c.LastName = @LastName;
END;

EXECUTE Sales.uspGetCustomers @FirstName = N'Pilar', @LastName = N'Ackerman';

WITH Customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Pilar', 'Ackerman', 'pilar0@adventure-works.com'),
            (2, 'Linda', 'Chen', 'linda1@adventure-works.com'),
            (3, 'David', 'Smith', 'david2@adventure-works.com')
    ) c (CustomerID, FirstName, LastName, EmailAddress)
)
SELECT *
FROM Customers;

-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspGetCustomers;
