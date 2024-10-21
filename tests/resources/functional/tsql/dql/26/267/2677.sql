--Query type: DQL
WITH temp_result AS (
    SELECT NCHAR(506) COLLATE Latin1_General_CI_AS AS [Uppercase],
           NCHAR(507) COLLATE Latin1_General_CI_AS AS [Lowercase]
)
SELECT [Uppercase],
       [Lowercase]
FROM temp_result;