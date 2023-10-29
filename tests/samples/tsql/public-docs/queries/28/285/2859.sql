-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/decompress-transact-sql?view=sql-server-ver16

SELECT _id,
    name,
    surname,
    datemodified,
    CAST(DECOMPRESS(info) AS NVARCHAR(MAX)) AS info
FROM player;