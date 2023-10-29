-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-for-clause-transact-sql?view=sql-server-ver16

SELECT CAST(
    (SELECT column1, column2
        FROM my_table
        FOR XML PATH('')
    )
        AS VARCHAR(MAX)
) AS XMLDATA ;