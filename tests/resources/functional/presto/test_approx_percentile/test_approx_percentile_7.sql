
-- presto sql:
SELECT approx_percentile(height, weight, ARRAY[0.25, 0.5, 0.75]) FROM people;

-- databricks sql:
SELECT approx_percentile(height, weight, ARRAY(0.25, 0.5, 0.75)) FROM people;

