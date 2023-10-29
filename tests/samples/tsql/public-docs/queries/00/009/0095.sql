-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16

-- Genealogy table
IF OBJECT_ID('dbo.Person','U') IS NOT NULL DROP TABLE dbo.Person;
GO
CREATE TABLE dbo.Person(ID int, Name VARCHAR(30), Mother INT, Father INT);
GO
INSERT dbo.Person
VALUES(1, 'Sue', NULL, NULL)
      ,(2, 'Ed', NULL, NULL)
      ,(3, 'Emma', 1, 2)
      ,(4, 'Jack', 1, 2)
      ,(5, 'Jane', NULL, NULL)
      ,(6, 'Bonnie', 5, 4)
      ,(7, 'Bill', 5, 4);
GO
-- Create the recursive CTE to find all of Bonnie's ancestors.
WITH Generation (ID) AS
(
-- First anchor member returns Bonnie's mother.
    SELECT Mother
    FROM dbo.Person
    WHERE Name = 'Bonnie'
UNION
-- Second anchor member returns Bonnie's father.
    SELECT Father
    FROM dbo.Person
    WHERE Name = 'Bonnie'
UNION ALL
-- First recursive member returns male ancestors of the previous generation.
    SELECT Person.Father
    FROM Generation, Person
    WHERE Generation.ID=Person.ID
UNION ALL
-- Second recursive member returns female ancestors of the previous generation.
    SELECT Person.Mother
    FROM Generation, dbo.Person
    WHERE Generation.ID=Person.ID
)
SELECT Person.ID, Person.Name, Person.Mother, Person.Father
FROM Generation, dbo.Person
WHERE Generation.ID = Person.ID;
GO