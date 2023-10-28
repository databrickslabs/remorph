select * 
    from (
         select branch_name
             from branch_offices
             ORDER BY monthly_sales DESC
             limit 3
         )
    ;