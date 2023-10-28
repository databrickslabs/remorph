select * from stock_price_history match_recognize(
    partition by company
    order by price_date
    measures
        match_number() as "MATCH_NUMBER",
        classifier() as cl
    all rows per match with unmatched rows
    pattern(OVERAVG+)
    define
        OVERAVG as price > avg(price) over (rows between unbounded
                                 preceding and unbounded following)
)
order by company, price_date;