--Query type: DQL
WITH temp_result AS (
    SELECT CONVERT(XML, '<root><book genre="Fiction"/></root>') AS xml_column
)
SELECT nref.value('@genre', 'VARCHAR(max)') AS book_genre
FROM temp_result
CROSS APPLY xml_column.nodes('//book') AS R(nref)