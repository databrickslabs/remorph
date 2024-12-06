-- tsql sql:
SELECT xCol.value('(//customer/lname)[1]', 'NVARCHAR(50)') AS LastName FROM (VALUES (CONVERT(XML, '<customer><lname>Smith</lname></customer>'))) AS T(xCol)
