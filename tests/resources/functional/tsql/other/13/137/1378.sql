-- tsql sql:
CREATE TABLE #TravelReport
(
    TravelerName VARCHAR(100),
    TravelerID VARCHAR(50),
    TripID INT IDENTITY(1,1) PRIMARY KEY,
    DepartureDate DATE,
    Destination VARCHAR(100),
    TotalCost DECIMAL(10, 2),
    Currency VARCHAR(10),
    Description VARCHAR(200)
);

INSERT INTO #TravelReport
(
    TravelerName,
    TravelerID,
    DepartureDate,
    Destination,
    TotalCost,
    Currency,
    Description
)
VALUES
(
    'John Doe',
    'TRV001',
    '2022-01-01',
    'New York',
    1000.00,
    'USD',
    'Business Trip'
),
(
    'Jane Doe',
    'TRV002',
    '2022-02-01',
    'London',
    800.00,
    'GBP',
    'Vacation'
);

SELECT *
FROM #TravelReport;

-- REMORPH CLEANUP: DROP TABLE #TravelReport;
