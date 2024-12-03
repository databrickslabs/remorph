--Query type: DQL
WITH files AS (
    SELECT 'file1' AS name, 'ROWS' AS type_desc, 1 AS file_id
    UNION ALL
    SELECT 'file2', 'LOG', 2
)
SELECT
    f.file_id,
    f.type_desc,
    f.name,
    FILEPROPERTYEX(f.name, 'BlobTier') AS BlobTier,
    FILEPROPERTYEX(f.name, 'AccountType') AS AccountType,
    FILEPROPERTYEX(f.name, 'IsInferredTier') AS IsInferredTier,
    FILEPROPERTYEX(f.name, 'IsPageBlob') AS IsPageBlob
FROM files AS f
WHERE f.type_desc IN ('ROWS', 'LOG');
