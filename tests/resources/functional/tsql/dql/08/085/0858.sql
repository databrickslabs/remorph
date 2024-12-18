-- tsql sql:
WITH temp_result AS ( SELECT regionkey, name, comment FROM ( VALUES (1, 'Region 1', 'Comment 1'), (2, 'Region 2', 'Comment 2') ) AS region(regionkey, name, comment) ) SELECT regionkey, name FROM temp_result;
