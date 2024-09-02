--Query type: DDL
CREATE TABLE #CustomerCTE (c_custkey INT, c_name VARCHAR(50), c_address VARCHAR(100));
CREATE UNIQUE INDEX AK_CustomerIndex ON #CustomerCTE (c_custkey) WITH (IGNORE_DUP_KEY = ON);