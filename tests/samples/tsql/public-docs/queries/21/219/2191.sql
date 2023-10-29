-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-ver16

INSERT INTO Cities (Location)  
VALUES ( CONVERT(Point, '12.3:46.2') );