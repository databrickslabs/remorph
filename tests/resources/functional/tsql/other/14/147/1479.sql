-- tsql sql:
DECLARE @MyCursor CURSOR;
SET @MyCursor = CURSOR LOCAL SCROLL FOR
    SELECT *
    FROM (
        VALUES (1, 'John', 'Doe'),
               (2, 'Jane', 'Doe'),
               (3, 'Bob', 'Smith')
    ) AS Customer(CustKey, CustName, CustAddress);
