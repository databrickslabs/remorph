-- see https://docs.snowflake.com/en/sql-reference/functions/is_binary

select v AS hex_encoded_binary_value 
    from varbin 
    where is_binary(v);