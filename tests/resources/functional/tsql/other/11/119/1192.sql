--Query type: DDL
CREATE TABLE Supplier (id INT, name VARCHAR(100), supplyCount INT, supplyDate DATE);
INSERT INTO Supplier (id, name, supplyCount, supplyDate)
VALUES (1, 'Supplier1', 10, '2020-01-01'), (2, 'Supplier2', 50, '2020-01-15'), (3, 'Supplier3', 100, '2020-02-01');
SELECT id, name, supplyCount, supplyDate, CASE WHEN supplyCount <= 10 THEN '0-10' WHEN supplyCount <= 50 THEN '11-50' WHEN supplyCount <= 100 THEN '51-100' WHEN supplyCount <= 200 THEN '101-200' ELSE '201+' END AS supplyRange
FROM Supplier;
SELECT * FROM Supplier;