-- tsql sql:
WITH CustomerCTE AS ( SELECT SUBSTRING(c_name, 1, 30) AS CustomerName, c_acctbal FROM (VALUES ('John', 100.0), ('Jane', 200.0)) AS Customer(c_name, c_acctbal) ) SELECT CustomerName, c_acctbal FROM CustomerCTE WHERE CAST(c_acctbal AS INT) LIKE '33%';
