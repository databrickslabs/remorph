--Query type: DQL
WITH temp_result AS (SELECT c_name, c_mktsegment FROM (VALUES ('name1', 'segment1'), ('name2', 'segment2')) AS temp_table(c_name, c_mktsegment)) SELECT TOP 10 * FROM temp_result WHERE c_mktsegment = 'BUILDING';
