SELECT province, o_col,
      'o_col < 15' AS condition,
      CONDITIONAL_CHANGE_EVENT(o_col) 
        OVER (PARTITION BY province ORDER BY o_col) 
          AS change_event,
      CONDITIONAL_CHANGE_EVENT(o_col < 15) 
        OVER (PARTITION BY province ORDER BY o_col) 
          AS change_event_2
    FROM table1
    ORDER BY province, o_col
    ;