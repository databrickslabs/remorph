-- tsql sql:
CREATE TABLE #Customer
(
    c_customerkey INT,
    c_comment VARCHAR(100)
);

INSERT INTO #Customer
(
    c_customerkey,
    c_comment
)
VALUES
(
    1,
    'Comment 1'
),
(
    2,
    'Comment 2'
);

CREATE FULLTEXT CATALOG ft AS DEFAULT;

CREATE FULLTEXT INDEX ON #Customer
(
    c_comment
)
KEY INDEX ui_ukCustomer
WITH STOPLIST = SYSTEM;

SELECT *
FROM #Customer;

-- REMORPH CLEANUP: DROP TABLE #Customer;
