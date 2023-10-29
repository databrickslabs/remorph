-- see https://docs.snowflake.com/en/sql-reference/functions/lpad

SELECT b, LPAD(b, 10, TO_BINARY(HEX_ENCODE(' '))) AS PAD_WITH_BLANK, 
          LPAD(b, 10, TO_BINARY(HEX_ENCODE('$'))) AS PAD_WITH_DOLLAR_SIGN 
    FROM demo
    ORDER BY b;