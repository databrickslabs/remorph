--Query type: DML
-- Create a table to store customer data
CREATE TABLE CustomerData
(
    CustomerID INT,
    TotalPurchase DECIMAL(10, 2),
    IsPremium BIT
);

-- Insert some sample data into the table
INSERT INTO CustomerData (CustomerID, TotalPurchase, IsPremium)
VALUES
    (1, 100.00, 0),
    (2, 200.00, 1),
    (3, 300.00, 0);

-- Create a CTE to update customer data
WITH UpdatedCustomerData AS (
    SELECT CustomerID,
           CASE
               WHEN (TotalPurchase - 100.00) < 0 THEN TotalPurchase + 50
               ELSE TotalPurchase + 20.00
           END AS NewTotalPurchase,
           IsPremium
    FROM CustomerData
)
-- Update the customer data using the CTE
UPDATE cd
SET TotalPurchase = ucd.NewTotalPurchase
OUTPUT Deleted.CustomerID,
       Deleted.TotalPurchase AS BeforeValue,
       Inserted.TotalPurchase AS AfterValue
FROM CustomerData cd
INNER JOIN UpdatedCustomerData ucd ON cd.CustomerID = ucd.CustomerID
WHERE cd.IsPremium = 0;

-- Select the updated data to show the results
SELECT * FROM CustomerData;

-- REMORPH CLEANUP: DROP TABLE CustomerData;
