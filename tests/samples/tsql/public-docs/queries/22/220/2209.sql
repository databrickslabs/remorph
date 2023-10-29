-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/compress-transact-sql?view=sql-server-ver16

INSERT INTO player (
    name,
    surname,
    info
    )
VALUES (
    N'Ovidiu',
    N'Cracium',
    COMPRESS(N'{"sport":"Tennis","age": 28,"rank":1,"points":15258, turn":17}')
    );

INSERT INTO player (
    name,
    surname,
    info
    )
VALUES (
    N'Michael',
    N'Raheem',
    COMPRESS(@info)
    );