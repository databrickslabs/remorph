--Query type: DDL
CREATE TABLE CustomerQueue
(
    CustomerSubmission nvarchar(255),
    CustomerProcessing nvarchar(255)
);

INSERT INTO CustomerQueue
(
    CustomerSubmission,
    CustomerProcessing
)
SELECT *
FROM
(
    VALUES
    (
        '//TPC-H.com/Customers/CustomerSubmission',
        '//TPC-H.com/Customers/CustomerProcessing'
    )
) AS temp_result
(
    CustomerSubmission,
    CustomerProcessing
);

SELECT *
FROM CustomerQueue;
-- REMORPH CLEANUP: DROP TABLE CustomerQueue;
