--Query type: DQL
WITH temp_result AS (SELECT 0xabcdef AS hex_value)
SELECT GET_BIT(hex_value, 2) AS Get_2nd_Bit, GET_BIT(hex_value, 4) AS Get_4th_Bit
FROM temp_result