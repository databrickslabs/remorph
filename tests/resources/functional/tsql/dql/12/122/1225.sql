-- tsql sql:
SELECT c_customerkey, c_name, c_address FROM (VALUES (1, 'Customer#000000001', '1313 Interiors Ave'), (2, 'Customer#000000002', '9110 Forest Ave'), (3, 'Customer#000000003', '7717 Saddle Dr')) AS customer (c_customerkey, c_name, c_address) WHERE c_address.value('(/root[@a=sql:column("c_customerkey")]/@a)[1]', 'integer') = c_customerkey;
