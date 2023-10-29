-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-library-transact-sql?view=sql-server-ver16

EXEC sp_execute_external_script
    @language = N'Java'
    , @script = N'customJar.MyCLass.myMethod'
    , @input_data_1 = N'SELECT * FROM dbo.MyTable'
WITH RESULT SETS ((column1 int))