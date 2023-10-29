-- see https://docs.snowflake.com/en/sql-reference/functions/as_boolean

SELECT AS_BOOLEAN(TO_VARIANT(TRUE)), AS_BOOLEAN(TO_VARIANT(FALSE)), AS_BOOLEAN(TO_VARIANT(NULL));