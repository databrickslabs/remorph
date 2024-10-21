--Query type: DQL
WITH requests AS (
    SELECT 'BACKUP DATABASE' AS command, 1000 AS estimated_completion_time, GETDATE() AS start_time
    UNION ALL
    SELECT 'BACKUP LOG', 2000, GETDATE() - 1
),
sql_text AS (
    SELECT 'BACKUP DATABASE' AS text
    UNION ALL
    SELECT 'BACKUP LOG'
)
SELECT 
    query = st.text, 
    start_time, 
    percent_complete = 50, 
    eta = DATEADD(second, r.estimated_completion_time/1000, GETDATE())
FROM requests r
CROSS APPLY sql_text st
WHERE r.command LIKE 'BACKUP%' ESCAPE '%';