-- see https://docs.snowflake.com/en/sql-reference/functions/rank

SELECT state, bushels,
        RANK() OVER (PARTITION BY state ORDER BY bushels DESC),
        DENSE_RANK() OVER (PARTITION BY state ORDER BY bushels DESC)
    FROM corn_production;