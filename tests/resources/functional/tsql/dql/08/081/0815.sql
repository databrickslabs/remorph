--Query type: DQL
SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS temp_table (i_col, s_col) ORDER BY i_col;
