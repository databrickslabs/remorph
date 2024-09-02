--Query type: DQL
WITH db_options AS (SELECT 'MyOptionsTest' AS name, 'SQL_Latin1_General_CP1_CI_AS' AS collation_name, 1 AS is_trustworthy_on, 1 AS is_db_chaining_on)
SELECT name, collation_name, is_trustworthy_on, is_db_chaining_on
FROM db_options
WHERE name = 'MyOptionsTest';