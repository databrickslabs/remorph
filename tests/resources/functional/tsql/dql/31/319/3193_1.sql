--Query type: DQL
SELECT DISTINCT T1.name FROM (VALUES ('John', 25), ('Alice', 30), ('Bob', 35)) AS T1 (name, age);