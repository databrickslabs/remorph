--Query type: DQL
WITH temp_result AS (SELECT 'Returns the length.' AS string_exp) SELECT {fn BIT_LENGTH(string_exp)} FROM temp_result