-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

select varchar1, 
       float1::varchar,
       variant1:"Loan Number"::varchar from tmp;