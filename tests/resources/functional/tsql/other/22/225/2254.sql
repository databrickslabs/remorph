-- tsql sql:
CREATE TABLE #master_files
(
    database_id INT,
    file_id INT,
    file_guid UNIQUEIDENTIFIER,
    type_desc NVARCHAR(60),
    data_space_id INT,
    name NVARCHAR(128),
    filename NVARCHAR(260),
    state_desc NVARCHAR(60),
    size INT,
    max_size INT,
    growth INT,
    is_media_read_only BIT,
    is_read_only BIT,
    is_sparse BIT,
    is_percent_growth BIT,
    is_name_reserved BIT,
    create_lsn INT,
    drop_lsn INT,
    read_only_lsn INT,
    read_write_lsn INT,
    differential_base_lsn INT,
    differential_base_guid UNIQUEIDENTIFIER,
    differential_base_create_date DATETIME,
    is_deleted BIT,
    is_offline BIT,
    has_replica_root BIT
);

INSERT INTO #master_files
(
    database_id,
    file_id,
    type_desc,
    name,
    filename
)
VALUES
(
    DB_ID('MyDatabase'),
    1,
    'ROWS',
    'MyDatabase_Data',
    'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\MyDatabase.mdf'
),
(
    DB_ID('MyDatabase'),
    2,
    'LOG',
    'MyDatabase_Log',
    'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\MyDatabase.ldf'
);

SELECT *
FROM #master_files
WHERE database_id = DB_ID('MyDatabase');
-- REMORPH CLEANUP: DROP TABLE #master_files;
