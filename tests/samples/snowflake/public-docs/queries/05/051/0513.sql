-- see https://docs.snowflake.com/en/sql-reference/functions/array_agg

CREATE TABLE orders (
    o_orderkey INTEGER,         -- unique ID for each order.
    o_clerk VARCHAR,            -- identifies which clerk is responsible.
    o_totalprice NUMBER(12, 2), -- total price.
    o_orderstatus CHAR(1)       -- 'F' = Fulfilled (sent); 
                                -- 'O' = 'Ordered but not yet Fulfilled'.
    );

INSERT INTO orders (o_orderkey, o_orderstatus, o_clerk, o_totalprice) 
  VALUES 
    ( 32123, 'O', 'Clerk#000000321',     321.23),
    ( 41445, 'F', 'Clerk#000000386', 1041445.00),
    ( 55937, 'O', 'Clerk#000000114', 1055937.00),
    ( 67781, 'F', 'Clerk#000000521', 1067781.00),
    ( 80550, 'O', 'Clerk#000000411', 1080550.00),
    ( 95808, 'F', 'Clerk#000000136', 1095808.00),
    (101700, 'O', 'Clerk#000000220', 1101700.00),
    (103136, 'F', 'Clerk#000000508', 1103136.00);