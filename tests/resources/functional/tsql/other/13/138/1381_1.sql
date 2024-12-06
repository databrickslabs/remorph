-- tsql sql:
WITH MyCTE AS (
    SELECT 'http://www.example.com/MySchema.xsd' AS SchemaUri
)
SELECT 'DROP XML SCHEMA COLLECTION MySchemaCollection;' AS DropStatement
FROM MyCTE
WHERE EXISTS (
    SELECT 1
    FROM (
        VALUES ('http://www.example.com/MySchema.xsd')
    ) AS T(SchemaUri)
    WHERE T.SchemaUri = MyCTE.SchemaUri
);
-- REMORPH CLEANUP: DROP XML SCHEMA COLLECTION MySchemaCollection;
