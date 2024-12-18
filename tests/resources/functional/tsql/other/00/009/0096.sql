-- tsql sql:
WITH sales_vw AS ( SELECT * FROM ( VALUES ('2022-01-01', 100), ('2022-01-02', 200) ) AS sales (sale_date, amount) ) SELECT * FROM sales_vw;
