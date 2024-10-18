--Query type: DQL
WITH certificates AS (
    SELECT thumbprint, name
    FROM (
        VALUES (
            0x1234567890abcdef, 'SchemaSigningCertificate1'
        ), (
            0x234567890abcdef1, 'SchemaSigningCertificate2'
        )
    ) AS t(thumbprint, name)
), objects AS (
    SELECT 'spt_fallback_db' AS objectname
)
SELECT o.objectname AS [object name], IS_OBJECTSIGNED('OBJECT', OBJECT_ID(o.objectname), 'certificate', c.thumbprint) AS [Is the object signed?]
FROM objects o
CROSS JOIN certificates c
WHERE c.name LIKE '%SchemaSigningCertificate%'