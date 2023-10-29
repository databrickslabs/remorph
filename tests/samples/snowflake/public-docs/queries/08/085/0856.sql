-- see https://docs.snowflake.com/en/sql-reference/constructs/pivot

SELECT * 
  FROM monthly_sales
    PIVOT(SUM(amount) FOR MONTH IN ('JAN', 'FEB', 'MAR', 'APR'))
      AS p (EMP_ID_renamed, JAN, FEB, MAR, APR)
  ORDER BY EMP_ID_renamed;