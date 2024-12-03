--Query type: DDL
ALTER DATABASE tempdb
ADD FILE (
    NAME = tempdev,
    FILENAME = 'C:\tempdb.mdf',
    SIZE = 5MB
);
