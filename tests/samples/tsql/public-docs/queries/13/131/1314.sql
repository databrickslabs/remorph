-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/decompress-transact-sql?view=sql-server-ver16

CREATE TABLE example_table (
    _id INT PRIMARY KEY IDENTITY,
    name NVARCHAR(MAX),
    surname NVARCHAR(MAX),
    info VARBINARY(MAX),
    info_json AS CAST(DECOMPRESS(info) AS NVARCHAR(MAX))
);