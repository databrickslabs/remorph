-- see https://docs.snowflake.com/en/sql-reference/functions/array_intersection

SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B', 'C'), 
                          ARRAY_CONSTRUCT('B', 'C'));