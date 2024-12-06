-- tsql sql:
CREATE TABLE orders_fact (
    o_orderkey INT NOT NULL CONSTRAINT ord_fact_pk PRIMARY KEY,
    o_custkey INT NOT NULL CONSTRAINT ord_fact_custkey_unique UNIQUE,
    o_orderstatus VARCHAR(10) NOT NULL,
    o_totalprice DECIMAL(10, 2) NOT NULL
);
