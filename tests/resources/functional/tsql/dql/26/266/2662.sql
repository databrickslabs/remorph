--Query type: DQL
SELECT LEN(c_name) AS Length, c_name, c_address, c_phone FROM (VALUES ('Customer#000000001', '1297.35.939.162.7', '25-989-741-6878715'), ('Customer#000000002', '1297.35.939.162.7', '25-989-741-6878715'), ('Customer#000000003', '1297.35.939.162.7', '25-989-741-6878715')) AS Customer(c_name, c_address, c_phone) WHERE c_name = 'Customer#000000001';
