--Query type: DQL
SELECT DATEFROMPARTS(o_orderyear, 12, 31) AS order_date FROM (VALUES (2010), (2011), (2012)) AS order_years (o_orderyear);