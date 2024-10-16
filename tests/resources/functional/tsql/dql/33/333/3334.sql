--Query type: DQL
SELECT nation_name, phone FROM (VALUES ('UNITED STATES', '123-456-7890'), ('CANADA', '987-654-3210')) AS region (nation_name, phone) WHERE ISNUMERIC(phone) <> 1;