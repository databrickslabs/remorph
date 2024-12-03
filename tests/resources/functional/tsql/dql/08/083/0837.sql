--Query type: DQL
SELECT * FROM (VALUES (1, 'John'), (2, 'Alice'), (3, 'Bob')) AS temp_result (id, name) ORDER BY id;
