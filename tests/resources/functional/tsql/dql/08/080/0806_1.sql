--Query type: DQL
SELECT UPPER(string) COLLATE Latin1_General_CI_AS AS collated_string
FROM (
    VALUES ('m')
) AS temp_table (string)
WHERE UPPER(string) COLLATE Latin1_General_CI_AS BETWEEN 'A' AND 'Z';
