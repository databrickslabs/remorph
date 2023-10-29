-- see https://docs.snowflake.com/en/sql-reference/functions/listagg

SELECT listagg(DISTINCT O_ORDERSTATUS, '|')
    FROM orders WHERE O_TOTALPRICE > 450000;
