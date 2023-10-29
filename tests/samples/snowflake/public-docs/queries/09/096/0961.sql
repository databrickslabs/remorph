-- see https://docs.snowflake.com/en/sql-reference/functions/arrays_overlap

SELECT ARRAYS_OVERLAP(ARRAY_CONSTRUCT(1, 2, NULL),
                      ARRAY_CONSTRUCT(3, NULL, 5))
 AS Overlap;