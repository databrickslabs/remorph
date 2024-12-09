-- snowflake sql:
WITH
    params(p) AS (SELECT 'i')
SELECT REGEXP_SUBSTR('The real world of The Doors', 'the\\W+\\w+', 1, 2, p) FROM params;

-- databricks sql:
WITH
    params (p) AS (SELECT 'i')
SELECT REGEXP_EXTRACT_ALL(
    SUBSTR('The real world of The Doors', 1),
    AGGREGATE(
        SPLIT(p, ''),
        CAST(ARRAY() AS ARRAY<STRING>),
        (agg, item) ->
            CASE
                WHEN item = 'c' THEN FILTER(agg, item -> item != 'i')
                WHEN item IN ('i', 's', 'm') THEN ARRAY_APPEND(agg, item)
                ELSE agg
            END
        ,
        filtered -> '(?' || ARRAY_JOIN(filtered, '') || ')' || 'the\\W+\\w+'
    ), 0)[1] FROM params;
