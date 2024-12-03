--Query type: DQL
SELECT STRING_AGG(CONVERT(NVARCHAR(max), CONCAT(c_name, ' ', c_address, '(', c_phone, ')')), CHAR(13)) AS customer_info FROM (VALUES ('Customer#000000001', '1313 Interiors Ave.', '25-989-741-2988'), ('Customer#000000002', '1855 Bayside Blvd.', '11-705-781-5278')) AS customers (c_name, c_address, c_phone);
