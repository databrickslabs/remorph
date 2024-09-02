--Query type: DQL
WITH temp_result AS ( SELECT 38 AS dividend, 5 AS divisor ) SELECT dividend / divisor AS Integer, dividend % divisor AS Remainder FROM temp_result;