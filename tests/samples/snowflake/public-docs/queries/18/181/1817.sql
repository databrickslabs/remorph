-- see https://docs.snowflake.com/en/sql-reference/functions/iff

SELECT val, IFF(val::int = val, 'integer', 'non-integer')
    FROM ( SELECT column1 as val
               FROM values(1.0), (1.1), (-3.1415), (-5.000), (null) )
    ORDER BY val DESC;