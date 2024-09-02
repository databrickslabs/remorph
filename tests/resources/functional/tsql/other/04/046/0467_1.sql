--Query type: DCL
DECLARE @region_name VARCHAR(255);
SELECT @region_name = 'Europe'
FROM (
    VALUES (
        1
    )
) AS dummy_table(dummy_column);

SELECT region_name
FROM (
    VALUES (@region_name)
) AS region_table(region_name);