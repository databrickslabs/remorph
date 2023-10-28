select price_date, match_number, msq, price, cl from
  (select * from stock_price_history where company='ABCD') match_recognize(
    order by price_date
    measures
        match_number() as "MATCH_NUMBER",
        match_sequence_number() as msq,
        classifier() as cl
    all rows per match
    pattern(ANY_ROW UP+)
    define
        ANY_ROW AS TRUE,
        UP as price > lag(price)
)
order by match_number, msq;