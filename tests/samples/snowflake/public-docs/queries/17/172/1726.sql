-- see https://docs.snowflake.com/en/sql-reference/functions/object_agg

SELECT seq, key, value
FROM (SELECT object_agg(k, v) o FROM objectagg_example GROUP BY g),
    LATERAL FLATTEN(input => o);
