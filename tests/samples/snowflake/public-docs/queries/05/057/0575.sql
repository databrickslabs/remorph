-- see https://docs.snowflake.com/en/sql-reference/sql/create-view

CREATE VIEW v1 (pre_tax_profit, taxes, after_tax_profit) AS
    SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
    FROM table1;