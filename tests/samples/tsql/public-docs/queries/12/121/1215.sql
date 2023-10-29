-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver16

CREATE TABLE OrdersHistory (
   id INT,
   city VARCHAR (25),
   lastUpdateDate DATE,
   orderDate DATE)
WITH
    (DISTRIBUTION = HASH (id),
    PARTITION ( orderDate RANGE RIGHT
    FOR VALUES ('2004-01-01'))) ;