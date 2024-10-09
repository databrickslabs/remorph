--Query type: DML
CREATE TABLE #Employee
(
    BusinessEntityID INT,
    PayFrequency INT
);

INSERT INTO #Employee
(
    BusinessEntityID,
    PayFrequency
)
VALUES
(
    1,
    2
),
(
    2,
    3
);

WITH E AS
(
    SELECT BusinessEntityID, PayFrequency
    FROM #Employee
)
UPDATE E
SET PayFrequency = 4
WHERE BusinessEntityID = 1;

IF @@ERROR = 547
BEGIN
    PRINT N'A check constraint violation occurred.';
END

SELECT *
FROM #Employee;

-- REMORPH CLEANUP: DROP TABLE #Employee;