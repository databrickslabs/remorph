--Query type: DQL
SELECT PARSE('Tuesday, 14 December 2010' AS datetime2 USING 'en-GB') AS Result
FROM (
    VALUES ('Tuesday, 14 December 2010')
) AS T(date_string);