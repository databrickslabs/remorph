-- see https://docs.snowflake.com/en/sql-reference/functions/round

select f, round(f, 2), 
       d, round(d, 2) 
    from rnd1 
    order by 1;