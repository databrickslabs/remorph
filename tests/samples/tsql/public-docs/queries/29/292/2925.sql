-- see https://learn.microsoft.com/en-us/sql/t-sql/xml/guidelines-for-using-xml-data-type-methods?view=sql-server-ver16

SELECT nref.value('@genre', 'VARCHAR(max)') LastName
FROM T CROSS APPLY xCol.nodes('//book') AS R(nref)