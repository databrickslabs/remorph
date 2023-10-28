DELETE tableA WHERE EXISTS (
SELECT TOP 1 1 FROM tableB tb WHERE tb.col1 = tableA.col1
)