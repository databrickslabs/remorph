-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/guidelines-for-using-xml-data-type-methods?view=sql-server-ver16

DECLARE @x XML
DECLARE @c VARCHAR(max)
SET @x = '<root>Hello</root>'
SET @c = @x.value('/root[1]', 'VARCHAR(11)')
PRINT @c