--Query type: DDL
CREATE TABLE Customer_Cluster
(
    c_custkey INT,
    c_nationkey INT,
    c_acctbal DECIMAL(10, 2)
);

INSERT INTO Customer_Cluster (c_custkey, c_nationkey, c_acctbal)
SELECT c_custkey, c_nationkey, c_acctbal
FROM (
    VALUES (1, 1, 100.00),
           (2, 2, 200.00)
) AS temp_table (c_custkey, c_nationkey, c_acctbal);

CREATE CLUSTERED INDEX IX_Customer_Cluster
ON Customer_Cluster (c_custkey, c_nationkey);

SELECT *
FROM Customer_Cluster;
