--Query type: DML
CREATE TABLE #JobApplicants
(
    JobApplicantID INT,
    Name VARCHAR(100),
    JobTitle VARCHAR(100)
);

INSERT INTO #JobApplicants
(
    JobApplicantID,
    Name,
    JobTitle
)
VALUES
(
    1,
    'John Doe',
    'Software Engineer'
),
(
    2,
    'Jane Smith',
    'Data Scientist'
),
(
    3,
    'Bob Johnson',
    'Product Manager'
);

DELETE FROM #JobApplicants
WHERE JobApplicantID = 2;

SELECT *
FROM #JobApplicants;

-- REMORPH CLEANUP: DROP TABLE #JobApplicants;
