--Query type: DQL
SELECT r_regionkey, r_name, n_name FROM (VALUES (0, 'AFRICA', 'ALGERIA'), (1, 'AMERICA', 'ARGENTINA'), (2, 'ASIA', 'ARGENTINA'), (3, 'EUROPE', 'ARGENTINA'), (4, 'MIDDLE EAST', 'ARGENTINA')) AS region (r_regionkey, r_name, n_name) ORDER BY r_regionkey OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY;
