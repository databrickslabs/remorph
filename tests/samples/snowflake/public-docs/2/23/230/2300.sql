CREATE TABLE store_profit (
    store_ID INTEGER, 
    province VARCHAR,
    profit NUMERIC(11, 2));
INSERT INTO store_profit (store_ID, province, profit) VALUES
    (1, 'Ontario', 300),
    (2, 'Saskatchewan', 250),
    (3, 'Ontario', 450),
    (4, 'Ontario', NULL)  -- hasn't opened yet, so no profit yet.
    ;