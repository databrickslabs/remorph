--Query type: DQL
SELECT ISJSON(temp_string) AS json_check FROM (VALUES ('new test string')) AS temp_table (temp_string);
