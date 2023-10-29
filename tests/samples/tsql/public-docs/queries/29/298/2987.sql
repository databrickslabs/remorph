-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/guidelines-for-using-xml-data-type-methods?view=sql-server-ver16

SELECT xCol.value('//author/last-name[1]', 'NVARCHAR(50)') LastName
FROM T