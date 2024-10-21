--Query type: DQL
SELECT pc_id, CHOOSE(pc_id, 'A', 'B', 'C', 'D', 'E') AS category_name FROM (VALUES (1), (2), (3), (4), (5)) AS categories (pc_id);