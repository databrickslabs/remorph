-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-sql-graph?view=sql-server-ver16

-- Create person node table
CREATE TABLE dbo.Person (ID integer PRIMARY KEY, name varchar(50)) AS NODE;
 
-- Insert records for Alice and John
INSERT INTO dbo.Person VALUES (1, 'Alice');
INSERT INTO dbo.Person VALUES (2,'John');