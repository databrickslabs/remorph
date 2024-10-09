--Query type: DDL
WITH mylib AS ( SELECT 'packageB.zip' AS library_name, 'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\' AS library_path ) SELECT * FROM mylib;