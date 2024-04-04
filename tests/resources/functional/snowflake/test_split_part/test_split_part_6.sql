
-- snowflake sql:
SELECT SPLIT_PART(col1, 'delim', len('abc'));

-- databricks sql:
SELECT SPLIT_PART(col1, 'delim', IF(LENGTH('abc') = 0, 1, LENGTH('abc')));
