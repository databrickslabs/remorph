--Query type: DQL
SELECT ProductID, RemovedDate FROM (VALUES (1, '2022-01-01'), (2, '2022-01-15'), (3, '2022-02-01')) AS RemovedProducts (ProductID, RemovedDate);