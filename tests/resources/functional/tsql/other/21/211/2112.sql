-- tsql sql:
CREATE TABLE #Customers
(
    ID INT,
    Name VARCHAR(100)
);

INSERT INTO #Customers (ID, Name)
VALUES
    (1, 'Customer1'),
    (2, 'Customer2'),
    (3, 'Customer3');

GRANT SELECT ON #Customers TO [TPC_H\Larry];

SELECT *
FROM #Customers;

-- REMORPH CLEANUP: DROP TABLE #Customers;
