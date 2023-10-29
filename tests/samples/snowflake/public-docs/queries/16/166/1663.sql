-- see https://docs.snowflake.com/en/sql-reference/functions/listagg

SELECT listagg(O_ORDERKEY, ' ')
    FROM orders WHERE O_TOTALPRICE > 450000;
