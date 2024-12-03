--Query type: DQL
WITH supplier_info AS ( SELECT 'Supplier#1' AS supplier_name, 'USA' AS nation, 'BUILDING' AS address_type UNION ALL SELECT 'Supplier#2', 'Canada', 'HOUSE' ) SELECT supplier_name FROM supplier_info WHERE supplier_name LIKE 'Supplier#%'
