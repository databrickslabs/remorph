SELECT name, status_date, late_balance AS "OVERDUE", 
        thirty_day_late_balance AS "30 DAYS OVERDUE",
        CONDITIONAL_CHANGE_EVENT(thirty_day_late_balance) 
          OVER (PARTITION BY name ORDER BY status_date) AS change_event_cnt,
        CONDITIONAL_TRUE_EVENT(thirty_day_late_balance) 
          OVER (PARTITION BY name ORDER BY status_date) AS true_cnt
    FROM borrowers
    ORDER BY name, status_date
    ;