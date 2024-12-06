-- snowflake sql:
SELECT
    b * c as new_b,
    a - new_b as ab_diff
FROM my_table
WHERE ab_diff >= 0;

-- databricks sql:
SELECT
    b * c as new_b,
    a - new_b as ab_diff
FROM my_table
WHERE a - b * c >= 0;
