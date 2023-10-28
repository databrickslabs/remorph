WITH RECURSIVE current_f (current_val, previous_val) AS
    (
    SELECT 0, 1
    UNION ALL 
    SELECT current_val + previous_val, current_val FROM current_f
      WHERE current_val + previous_val < 100
    )
  SELECT current_val FROM current_f ORDER BY current_val;