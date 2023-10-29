-- see https://docs.snowflake.com/en/sql-reference/functions/listagg

SELECT O_ORDERSTATUS, listagg(O_CLERK, ', ') WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)
    FROM orders WHERE O_TOTALPRICE > 450000 GROUP BY O_ORDERSTATUS;
