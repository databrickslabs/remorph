-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

USE tempdb;
GO

IF EXISTS (
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = 'mytbl2'
        )
    DROP TABLE mytbl2;
GO

USE tempdb;
GO

CREATE TABLE mytbl2 (c1 SYSNAME);
GO

INSERT mytbl2
VALUES ('Discount is 10-15% off'),
    ('Discount is .10-.15 off');
GO

SELECT c1
FROM mytbl2
WHERE c1 LIKE '%10-15!% off%' ESCAPE '!';
GO