-- tsql sql:
WITH temp_result AS (SELECT CAST('<root><author><last-name>Smith</last-name></author></root>' AS xml) AS xCol)
SELECT xCol.value('(//author/last-name/text())[1]', 'nvarchar(50)') AS AuthorName
FROM temp_result
