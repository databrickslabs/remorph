SELECT CAST(
    (SELECT column1, column2
        FROM my_table
        FOR XML PATH('')
    )
        AS VARCHAR(MAX)
) AS XMLDATA ;