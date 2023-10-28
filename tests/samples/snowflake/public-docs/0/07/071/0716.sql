SELECT column1 AS orig_string,
       TO_DECIMAL(column1, '$999.00') AS num,
       TO_DECIMAL(column1, '$999.00', 5, 2) AS num_with_scale,
       TO_DECIMAL(column1, 5, 2) AS num_with_format_err
  FROM VALUES ('$345.12');