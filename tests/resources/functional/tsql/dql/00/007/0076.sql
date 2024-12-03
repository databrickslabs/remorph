--Query type: DQL
WITH input_data AS ( SELECT o_orderdate, o_totalprice FROM orders WHERE o_orderdate >= '1992-01-01' AND o_orderdate < '1992-01-02' ) SELECT * FROM input_data AS id CROSS APPLY forecast_model(id.o_orderdate, id.o_totalprice) AS fm;
