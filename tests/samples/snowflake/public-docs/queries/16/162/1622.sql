-- see https://docs.snowflake.com/en/sql-reference/constructs/from

SELECT description, retail_price, wholesale_cost 
    FROM temporary_doc_test.ftable1;