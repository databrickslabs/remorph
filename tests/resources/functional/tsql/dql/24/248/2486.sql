--Query type: DQL
SELECT CONVERT(XML, x.string) FROM (VALUES ('<root><child/></root>')) AS x(string);