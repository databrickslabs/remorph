-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/compress-transact-sql?view=sql-server-ver16

DELETE
FROM player
OUTPUT deleted.id,
    deleted.name,
    deleted.surname,
    deleted.datemodifier,
    COMPRESS(deleted.info)
INTO dbo.inactivePlayers
WHERE datemodified < @startOfYear;