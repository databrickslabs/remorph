-- see https://docs.snowflake.com/en/sql-reference/constructs/match_recognize

SELECT company, price_date, price, "FINAL FIRST(LT45.price)", "FINAL LAST(LT45.price)"
    FROM stock_price_history
       MATCH_RECOGNIZE (
           PARTITION BY company
           ORDER BY price_date
           MEASURES
               FINAL FIRST(LT45.price) AS "FINAL FIRST(LT45.price)",
               FINAL LAST(LT45.price)  AS "FINAL LAST(LT45.price)"
           ALL ROWS PER MATCH
           AFTER MATCH SKIP PAST LAST ROW
           PATTERN (LT45 LT45)
           DEFINE
               LT45 AS price < 45.00
           )
    WHERE company = 'ABCD'
    ORDER BY price_date;