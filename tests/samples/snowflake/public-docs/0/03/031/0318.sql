SELECT
       TIME_SLICE(billing_date, 2, 'WEEK', 'START') AS "START OF SLICE",
       TIME_SLICE(billing_date, 2, 'WEEK', 'END')   AS "END OF SLICE",
       COUNT(*) AS "NUMBER OF LATE BILLS",
       SUM(balance_due) AS "SUM OF MONEY OWED"
    FROM accounts
    WHERE balance_due > 0    -- bill hasn't yet been paid
    GROUP BY "START OF SLICE", "END OF SLICE";