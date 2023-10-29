-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-sql-graph?view=sql-server-ver16

CREATE TABLE Person (
        ID INTEGER PRIMARY KEY, 
        name VARCHAR(100), 
        email VARCHAR(100)
 ) AS NODE;