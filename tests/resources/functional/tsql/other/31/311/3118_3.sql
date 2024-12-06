-- tsql sql:
CREATE TABLE #JobCandidate
(
    JobCandidateID INT,
    Name VARCHAR(50)
);

INSERT INTO #JobCandidate
(
    JobCandidateID,
    Name
)
VALUES
(
    13,
    'John Doe'
),
(
    14,
    'Jane Doe'
);

DELETE FROM #JobCandidate
WHERE JobCandidateID = 13;

SELECT *
FROM #JobCandidate
WHERE JobCandidateID <> 13;

-- REMORPH CLEANUP: DROP TABLE #JobCandidate;
