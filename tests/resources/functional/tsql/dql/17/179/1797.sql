--Query type: DQL
WITH temp_result AS ( SELECT 5 AS height, 1 AS radius ) SELECT PI() * SQUARE(radius) * height AS [Cyl Vol] FROM temp_result;
