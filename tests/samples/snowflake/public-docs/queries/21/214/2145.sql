-- see https://docs.snowflake.com/en/sql-reference/constructs/order-by

select * 
    from (
         select branch_name
             from branch_offices
             ORDER BY monthly_sales DESC
             limit 3
         )
    ;