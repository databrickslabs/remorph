--Query type: DQL
SELECT p_partkey, p_name, value FROM (VALUES (1, 'Part 1', 'tag1,tag2,tag3'), (2, 'Part 2', 'tag4,tag5,tag6')) AS p (p_partkey, p_name, tags) CROSS APPLY STRING_SPLIT(tags, ',');
