--Query type: DQL
SELECT CHECKSUM_AGG(CAST(o_orderpriority AS INT)) FROM (VALUES (1, 'HIGH'), (2, 'MEDIUM'), (3, 'LOW')) AS orders (o_orderkey, o_orderpriority);