--Query type: DQL
SELECT IDENT_CURRENT('customer') AS Current_Identity FROM (VALUES (1), (2), (3)) AS temp_table (id);