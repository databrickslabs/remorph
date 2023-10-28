SELECT EMPID AS EMP_ID, "'JAN'" AS JANUARY, "'FEB'" AS FEBRUARY, "'MAR'" AS MARCH,
    "'APR'" AS APRIL
  FROM monthly_sales
    PIVOT(sum(amount) FOR MONTH IN ('JAN', 'FEB', 'MAR', 'APR')) 
      AS p
  ORDER BY EMPID;