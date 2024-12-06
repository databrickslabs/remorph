-- tsql sql:
CREATE TABLE #customer_view
(
    c_custkey INT,
    c_name VARCHAR(255),
    c_address VARCHAR(255)
);

INSERT INTO #customer_view (c_custkey, c_name, c_address)
VALUES
    (1, 'John Doe', '123 Main St'),
    (2, 'Jane Doe', '456 Elm St');

CREATE CLUSTERED INDEX IDX_CL_customer_view
ON #customer_view (c_custkey);

SELECT *
FROM #customer_view;

-- REMORPH CLEANUP: DROP TABLE #customer_view;
