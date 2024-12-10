-- tsql sql:
SELECT * FROM (VALUES (1, 'value1', '2022-01-01', 10), (2, 'value2', '2022-01-02', 20)) AS temp_table (column_a, column_b, column_c, column_d);
