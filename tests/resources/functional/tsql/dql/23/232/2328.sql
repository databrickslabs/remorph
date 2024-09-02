--Query type: DQL
WITH tmp_fct AS ( SELECT * FROM ( VALUES (1, 'a'), (2, 'b') ) AS t (c_customerkey, c_name) ) SELECT * INTO #tmp_fct FROM tmp_fct