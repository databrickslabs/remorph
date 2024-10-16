--Query type: DQL
SELECT @@VERSION AS 'SQL Server Version'
FROM (
    VALUES (
        1
    )
) AS temp_result_set (
    single_column
);