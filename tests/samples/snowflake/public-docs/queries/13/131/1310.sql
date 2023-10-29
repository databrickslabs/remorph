-- see https://docs.snowflake.com/en/sql-reference/functions/seq1

SELECT ROW_NUMBER() OVER (ORDER BY seq4()) 
    FROM TABLE(generator(rowcount => 10));