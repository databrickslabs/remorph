-- tsql sql:
SET LANGUAGE French;
SELECT *
FROM (
    VALUES ('Hello', 'World')
) AS Message (
    Greeting,
    Text
);
