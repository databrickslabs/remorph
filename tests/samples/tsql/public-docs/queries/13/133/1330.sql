-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

CREATE TABLE t1
(
    c1 INT,
    index IX1 (c1) WHERE c1 > 0
);