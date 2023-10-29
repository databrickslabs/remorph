-- see https://docs.snowflake.com/en/sql-reference/constructs/match_recognize

select * from stock_price_history match_recognize(
    partition by company
    order by price_date
    measures
        match_number() as "MATCH_NUMBER"
    all rows per match omit empty matches
    pattern(OVERAVG*)
    define
        OVERAVG as price > avg(price) over (rows between unbounded
                                  preceding and unbounded following)
)
order by company, price_date;