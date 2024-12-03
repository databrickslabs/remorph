--Query type: DQL
SELECT * FROM (VALUES ('/decades/1950s/*.parquet'), ('/decades/1960s/*.parquet'), ('/decades/1970s/*.parquet')) AS temp_result (value);
