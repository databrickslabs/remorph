-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/guidelines-for-using-xml-data-type-methods?view=sql-server-ver16

DECLARE @x XML
SET @x = '<root>Hello</root>'
PRINT @x.value('/root[1]', 'varchar(20)') -- will not work because this is treated as a subquery (select top 1 col from table)