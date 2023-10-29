-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_true_event

SELECT province, o_col, 
      CONDITIONAL_TRUE_EVENT(o_col) 
        OVER (PARTITION BY province ORDER BY o_col) 
          AS true_event,
      CONDITIONAL_TRUE_EVENT(o_col > 20) 
        OVER (PARTITION BY province ORDER BY o_col) 
          AS true_event_gt_20
    FROM table1
    ORDER BY province, o_col
    ;