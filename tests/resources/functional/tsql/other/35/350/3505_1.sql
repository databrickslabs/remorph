--Query type: DDL
SELECT *
FROM (
    VALUES
        ('BlobStore3', 'C:\BlobStore\BlobStore3.mdf', 100, 'UNLIMITED', 1),
        ('FS5', 'C:\BlobStore\FS5', 'UNLIMITED', NULL, NULL),
        ('FS6', 'C:\BlobStore\FS6', 100, 'UNLIMITED', NULL)
) AS temp_result_set (name, filename, size, maxsize, filegrowth);
