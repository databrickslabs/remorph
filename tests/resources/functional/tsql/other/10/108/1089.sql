--Query type: DML
CREATE PROCEDURE InsertCustomer
    @CustomerKey INT,
    @Name VARCHAR(255)
AS
BEGIN
    INSERT INTO Customer (CustomerKey, Name)
    VALUES (@CustomerKey, @Name);
END;

EXEC InsertCustomer
    @CustomerKey = 1,
    @Name = 'Test Customer';

SELECT CustomerKey, Name
FROM (
    VALUES (1, 'Test Customer')
) AS Customer(CustomerKey, Name)
WHERE CustomerKey = 1;

-- REMORPH CLEANUP: DROP PROCEDURE InsertCustomer;
