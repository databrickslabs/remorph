--Query type: DQL
SELECT ISDATE(date_string) AS is_valid_date FROM (VALUES ('04/15/2008'), ('04-15-2008'), ('04.15.2008'), ('04/2008/15')) AS dates (date_string);