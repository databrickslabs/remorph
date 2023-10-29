-- see https://docs.snowflake.com/en/sql-reference/constructs/pivot

SELECT * 
  FROM monthly_sales
    PIVOT(SUM(amount) FOR MONTH IN ('JAN', 'FEB', 'MAR', 'APR'))
      AS p
  ORDER BY EMPID;