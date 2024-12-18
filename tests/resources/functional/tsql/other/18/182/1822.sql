-- tsql sql:
CREATE TABLE loan_applications
(
    c1 INT,
    c2 INT,
    c3 INT,
    c4 INT,
    score FLOAT
);

CREATE TABLE scoring_model
(
    model_name VARCHAR(50),
    model VARBINARY(max)
);

INSERT INTO scoring_model (model_name, model)
VALUES ('ScoringModelV1', 0x1234567890ABCDEF);

DECLARE @model VARBINARY(max) = (SELECT model FROM scoring_model WHERE model_name = 'ScoringModelV1');

WITH mytable AS
(
    SELECT 1 AS c1, 2 AS c2, 3 AS c3, 4 AS c4
    UNION ALL
    SELECT 5 AS c1, 6 AS c2, 7 AS c3, 8 AS c4
),
    scored_data AS
(
    SELECT c1, c2, c3, c4, (c1 + c2 + c3 + c4) / 4.0 AS score
    FROM mytable
)
INSERT INTO loan_applications (c1, c2, c3, c4, score)
SELECT c1, c2, c3, c4, score
FROM scored_data;

SELECT *
FROM loan_applications;

-- REMORPH CLEANUP: DROP TABLE loan_applications;
-- REMORPH CLEANUP: DROP TABLE scoring_model;
