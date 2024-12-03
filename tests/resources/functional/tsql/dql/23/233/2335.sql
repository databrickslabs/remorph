--Query type: DQL
SELECT *
FROM (
    VALUES (
        '2022-01-01 12:00:00', 'Diagnostic 1'),
        ('2022-01-02 13:00:00', 'Diagnostic 2'),
        ('2022-01-03 14:00:00', 'Diagnostic 3')
    ) AS Diagnostics (
        DateTimePublished,
        DiagnosticName
    )
ORDER BY DateTimePublished;
