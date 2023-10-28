SELECT column1 AS orig_string,
       TRY_TO_DECIMAL(column1) AS dec,
       TRY_TO_DECIMAL(column1, 10, 2) AS dec_with_scale,
       TRY_TO_DECIMAL(column1, 4, 2) AS dec_with_range_err
  FROM VALUES ('345.123');