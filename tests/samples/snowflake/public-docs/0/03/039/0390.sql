SELECT column1 date_1, column2 date_2,
      DATEDIFF(year, column1, column2) diff_years,
      DATEDIFF(month, column1, column2) diff_months,
      DATEDIFF(day, column1, column2) diff_days,
      column2::DATE - column1::DATE AS diff_days_via_minus
    FROM VALUES
      ('2015-12-30', '2015-12-31'),
      ('2015-12-31', '2016-01-01'),
      ('2016-01-01', '2017-12-31'),
      ('2016-08-23', '2016-09-07');