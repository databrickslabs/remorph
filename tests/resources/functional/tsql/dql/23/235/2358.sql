--Query type: DQL
SELECT * FROM (VALUES (1, 'value1'), (2, 'value2')) AS temp_result (part_id, other_column) ORDER BY part_id;
