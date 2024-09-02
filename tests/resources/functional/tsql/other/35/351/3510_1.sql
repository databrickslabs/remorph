--Query type: DDL
ALTER DATABASE TPC_H_DB
ADD FILE (
    NAME = TPC_H_FILE1,
    FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\tpc_h_file1.ndf',
    SIZE = 10MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 10MB
);